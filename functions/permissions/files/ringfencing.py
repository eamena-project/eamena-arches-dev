import uuid
from django.core.exceptions import ValidationError
from arches.app.functions.base import BaseFunction
from arches.app.models import models
from arches.app.models.resource import Resource
from django.contrib.auth.models import User, Group, Permission
from arches.app.models.tile import Tile
import json
import logging

from arches.app.utils.permission_backend import (
    get_restricted_users,
    get_groups_for_object)

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

logger = logging.getLogger(__name__)

""" 
A function designed to apply resource instance permissions en masse, based upon that resource containing
a specified concept(s). 

Data required from front-end component:
1. Nodegroup id                                selected_nodegroup
2. Node id                                     target_node
3. Concept id(s)                               select_val
4. Group + boolean access pairs                user_groups
"""

details = {
    "name": "Ringfencing",
    "type": "node",
    "description": "Function to control user access based on node value",
    "defaultconfig": {"triggering_nodegroups":[], "rules":[]},
    "classname": "Ringfencing",
    "component": "views/components/functions/ringfencing",
    "functionid": "be239b0a-145d-4e27-bb71-beaa855dcc11"
}


class Ringfencing(BaseFunction):

    def get(self):
        raise NotImplementedError

    def save(self, tile, request):
        data = tile.data
        rules = self.config['rules']
        # node = self.config['selected_node']
        # value = self.config['selected_val']
        # identities = self.config['user_groups']

        
        if len(rules) > 0:
            for rule in rules:
                # Check if tile.data has selectedNode and selectedVal
                if  data[rule['selectedNode']] and data[rule['selectedNode']] in rule['selectedVal']:

                    # Get the resource that is currently being saved
                    resource_instance = models.ResourceInstance.objects.get(pk=tile.resourceinstance_id)
                    resource = Resource.objects.get(pk=tile.resourceinstance_id)

                    # Get a dictionary of users id's with ANY restrictions on the resource
                    current_perms = get_restricted_users(resource)
   
                    # Get a dictionary of users with 'no_access' restriction on the current resource
                    current_restricted_users = {User.objects.get(pk=userid) for userid in current_perms['no_access']}
                    
                    # Check who should not have access to current resource based on the current rule
                    new_restricted_users = {User.objects.get(pk=_user['identityId']) for _user in rule['userGroups'] if _user['identityType'] == 'user' and not _user['identityVal']}
                  
                    users_to_allow = list(current_restricted_users - new_restricted_users)
                    users_to_restrict = list(new_restricted_users - current_restricted_users)
            
                    for identityModel in (users_to_restrict):# + groups_to_restrict):
                        # first remove all the current permissions
                        for perm in get_perms(identityModel, resource_instance):
                            remove_perm(perm, identityModel, resource_instance)

                        assign_perm("no_access_to_resourceinstance", identityModel, resource_instance)

                    for identityModel in (users_to_allow): 
                        # first remove all the current permissions
                        for perm in get_perms(identityModel, resource_instance):
                            remove_perm(perm, identityModel, resource_instance)

                    resource = Resource(str(resource_instance.resourceinstanceid))
                    resource.index()


# write test, verify that the resource instance permissions are as expected. 
# call ES, get instance and check it is indexed as expected 
# call django gaurdian get_group_perms + get_user_perms,


    # def delete(self, tile, request):
    #     raise NotImplementedError

    # def on_import(self, tile):
    #     raise NotImplementedError

    # def after_function_save(self, functionxgraph, request):
    #     raise NotImplementedError
