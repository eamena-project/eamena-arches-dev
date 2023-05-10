"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import json
import uuid

from distutils.util import strtobool

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.models import User, Group, Permission
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import View
from arches import __version__
from arches.app.models import models
from arches.app.models.card import Card
from arches.app.models.graph import Graph
from arches.app.models.tile import Tile
from arches.app.models.resource import Resource, ModelInactiveError
from arches.app.models.system_settings import settings
from arches.app.utils.activity_stream_jsonld import ActivityStreamCollection
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.utils.decorators import group_required
from arches.app.utils.decorators import can_edit_resource_instance
from arches.app.utils.decorators import can_delete_resource_instance
from arches.app.utils.decorators import can_read_resource_instance
from arches.app.utils.pagination import get_paginator
from arches.app.utils.permission_backend import (
    user_is_resource_editor,
    user_is_resource_reviewer,
    user_can_delete_resource,
    user_can_edit_resource,
    user_can_read_resource,
)
from arches.app.utils.response import JSONResponse, JSONErrorResponse
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.search.elasticsearch_dsl_builder import Query, Terms
from arches.app.search.mappings import RESOURCES_INDEX
from arches.app.views.base import BaseManagerView, MapBaseManagerView
from arches.app.views.concept import Concept
from arches.app.datatypes.datatypes import DataTypeFactory
from elasticsearch import Elasticsearch
from guardian.shortcuts import (
    assign_perm,
    get_perms,
    remove_perm,
    get_group_perms,
    get_user_perms,
    get_groups_with_perms,
    get_users_with_perms,
    get_perms_for_model,
)
import logging

logger = logging.getLogger(__name__)

def get_instance_creator(resource_instance, user=None):
    creatorid = None
    can_edit = None
    if models.EditLog.objects.filter(resourceinstanceid=resource_instance.resourceinstanceid).filter(edittype="create").exists():
        creatorid = (
            models.EditLog.objects.filter(resourceinstanceid=resource_instance.resourceinstanceid).filter(edittype="create")[0].userid
        )
    if creatorid is None or creatorid == "":
        creatorid = settings.DEFAULT_RESOURCE_IMPORT_USER["userid"]
    if user:
        can_edit = user.id == int(creatorid) or user.is_superuser
    return {"creatorid": creatorid, "user_can_edit_instance_permissions": can_edit}
    
def get_resource_relationship_types():
    resource_relationship_types = Concept().get_child_collections("00000000-0000-0000-0000-000000000005")
    default_relationshiptype_valueid = None
    for relationship_type in resource_relationship_types:
        if relationship_type[0] == "00000000-0000-0000-0000-000000000007":
            default_relationshiptype_valueid = relationship_type[2]
    relationship_type_values = {
        "values": [{"id": str(c[2]), "text": str(c[1])} for c in resource_relationship_types],
        "default": str(default_relationshiptype_valueid),
    }
    return relationship_type_values

@method_decorator(group_required("Resource Editor"), name="dispatch")
class ResourceEditorView(MapBaseManagerView):
    action = None

    @method_decorator(can_edit_resource_instance, name="dispatch")
    def get(
        self,
        request,
        graphid=None,
        resourceid=None,
        view_template="views/resource/editor.htm",
        main_script="views/resource/editor",
        nav_menu=True,
    ):
        if self.action == "copy":
            return self.copy(request, resourceid)

        logger.warning("in custom view")
        creator = None
        user_created_instance = None
        if resourceid is None:
            resource_instance = None
            graph = models.GraphModel.objects.get(pk=graphid)
            resourceid = ""
        else:
            resource_instance = Resource.objects.get(pk=resourceid)
            graph = resource_instance.graph
            instance_creator = get_instance_creator(resource_instance, request.user)
            creator = instance_creator["creatorid"]
            user_created_instance = instance_creator["user_can_edit_instance_permissions"]
        nodes = graph.node_set.all()
        resource_graphs = (
            models.GraphModel.objects.exclude(pk=settings.SYSTEM_SETTINGS_RESOURCE_MODEL_ID)
            .exclude(isresource=False)
            .exclude(isactive=False)
        )
        ontologyclass = [node for node in nodes if node.istopnode is True][0].ontologyclass or ""
        relationship_type_values = get_resource_relationship_types()
        nodegroups = []
        editable_nodegroups = []
        for node in nodes:
            if node.is_collector:
                added = False
                if request.user.has_perm("write_nodegroup", node.nodegroup):
                    editable_nodegroups.append(node.nodegroup)
                    nodegroups.append(node.nodegroup)
                    added = True
                if not added and request.user.has_perm("read_nodegroup", node.nodegroup):
                    nodegroups.append(node.nodegroup)

        nodes = nodes.filter(nodegroup__in=nodegroups)
        cards = graph.cardmodel_set.order_by("sortorder").filter(nodegroup__in=nodegroups).prefetch_related("cardxnodexwidget_set")
        cardwidgets = [
            widget for widgets in [card.cardxnodexwidget_set.order_by("sortorder").all() for card in cards] for widget in widgets
        ]
        widgets = models.Widget.objects.all()
        card_components = models.CardComponent.objects.all()
        applied_functions = JSONSerializer().serialize(models.FunctionXGraph.objects.filter(graph=graph))
        datatypes = models.DDataType.objects.all()
        user_is_reviewer = user_is_resource_reviewer(request.user)
        is_system_settings = False

        if resource_instance is None:
            tiles = []
            displayname = _("New Resource")
        else:
            displayname = resource_instance.displayname
            if displayname == "undefined":
                displayname = _("Unnamed Resource")
            if str(resource_instance.graph_id) == settings.SYSTEM_SETTINGS_RESOURCE_MODEL_ID:
                is_system_settings = True
                displayname = _("System Settings")

            tiles = resource_instance.tilemodel_set.order_by("sortorder").filter(nodegroup__in=nodegroups)
            provisionaltiles = []
            for tile in tiles:
                append_tile = True
                isfullyprovisional = False
                if tile.provisionaledits is not None:
                    if len(list(tile.provisionaledits.keys())) > 0:
                        if len(tile.data) == 0:
                            isfullyprovisional = True
                        if user_is_reviewer is False:
                            if str(request.user.id) in tile.provisionaledits:
                                tile.provisionaledits = {str(request.user.id): tile.provisionaledits[str(request.user.id)]}
                                tile.data = tile.provisionaledits[str(request.user.id)]["value"]
                            else:
                                if isfullyprovisional is True:
                                    # if the tile IS fully provisional and the current user is not the owner,
                                    # we don't send that tile back to the client.
                                    append_tile = False
                                else:
                                    # if the tile has authoritaive data and the current user is not the owner,
                                    # we don't send the provisional data of other users back to the client.
                                    tile.provisionaledits = None
                if append_tile is True:
                    provisionaltiles.append(tile)
            tiles = provisionaltiles
        map_layers = models.MapLayer.objects.all()
        map_markers = models.MapMarker.objects.all()
        map_sources = models.MapSource.objects.all()
        geocoding_providers = models.Geocoder.objects.all()
        templates = models.ReportTemplate.objects.all()

        cards = JSONSerializer().serializeToPython(cards)
        editable_nodegroup_ids = [str(nodegroup.pk) for nodegroup in editable_nodegroups]
        for card in cards:
            card["is_writable"] = False
            if str(card["nodegroup_id"]) in editable_nodegroup_ids:
                card["is_writable"] = True
        can_delete = user_can_delete_resource(request.user, resourceid)
        context = self.get_context_data(
            main_script=main_script,
            resourceid=resourceid,
            displayname=displayname,
            graphid=graph.graphid,
            graphiconclass=graph.iconclass,
            graphname=graph.name,
            ontologyclass=ontologyclass,
            resource_graphs=resource_graphs,
            relationship_types=relationship_type_values,
            widgets=widgets,
            widgets_json=JSONSerializer().serialize(widgets),
            card_components=card_components,
            card_components_json=JSONSerializer().serialize(card_components),
            tiles=JSONSerializer().serialize(tiles),
            cards=JSONSerializer().serialize(cards),
            applied_functions=applied_functions,
            nodegroups=JSONSerializer().serialize(nodegroups),
            nodes=JSONSerializer().serialize(nodes),
            cardwidgets=JSONSerializer().serialize(cardwidgets),
            datatypes_json=JSONSerializer().serialize(datatypes, exclude=["iconclass", "modulename", "classname"]),
            map_layers=map_layers,
            map_markers=map_markers,
            map_sources=map_sources,
            geocoding_providers=geocoding_providers,
            user_is_reviewer=json.dumps(user_is_reviewer),
            user_can_delete_resource=can_delete,
            creator=json.dumps(creator),
            user_created_instance=json.dumps(user_created_instance),
            report_templates=templates,
            templates_json=JSONSerializer().serialize(templates, sort_keys=False, exclude=["name", "description"]),
            graph_json=JSONSerializer().serialize(graph),
            is_system_settings=is_system_settings,
        )

        context["nav"]["title"] = ""
        context["nav"]["menu"] = nav_menu
        if resourceid == settings.RESOURCE_INSTANCE_ID:
            context["nav"]["help"] = {"title": _("Managing System Settings"), "template": "system-settings-help"}
        else:
            context["nav"]["help"] = {"title": _("Using the Resource Editor"), "template": "resource-editor-help"}

        return render(request, view_template, context)

    @method_decorator(group_required("Resource Deleter"), name="dispatch")
    def delete(self, request, resourceid=None):
        delete_error = _("Unable to Delete Resource")
        delete_msg = _("User does not have permissions to delete this instance because the instance or its data is restricted")
        try:
            if resourceid is not None:
                if user_can_delete_resource(request.user, resourceid) is False:
                    return JSONErrorResponse(delete_error, delete_msg)
                ret = Resource.objects.get(pk=resourceid)
                try:
                    deleted = ret.delete(user=request.user)
                except ModelInactiveError as e:
                    message = _("Unable to delete. Please verify the model status is active")
                    return JSONResponse({"status": "false", "message": [_(e.title), _(str(message))]}, status=500)
                except PermissionDenied:
                    return JSONErrorResponse(delete_error, delete_msg)
                if deleted is True:
                    return JSONResponse(ret)
                else:
                    return JSONErrorResponse(delete_error, delete_msg)
            return HttpResponseNotFound()
        except PermissionDenied:
            return JSONErrorResponse(delete_error, delete_msg)


    def copy(self, request, resourceid=None):
        resource_instance = Resource.objects.get(pk=resourceid)
        return JSONResponse(resource_instance.copy())



