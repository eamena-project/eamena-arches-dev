|**table_name|columns|
|--|--|
|**auth_group**|name, id|
|**auth_group_permissions**|permission_id, group_id, id|
|**auth_permission**|content_type_id, codename, name, id|
|**auth_user**|email, password, last_login, first_name, username, date_joined, is_active, is_staff, id, last_name, is_superuser|
|**auth_user_groups**|id, group_id, user_id|
|**auth_user_user_permissions**|id, permission_id, user_id|
|**card_components**|defaultconfig, componentid, description, name, componentname, component|
|**card_constraints**|uniquetoallinstances, constraintid, cardid|
|**cards**|componentid, cssclass, description, sortorder, visible, active, helptext, helptitle, helpenabled, instructions, cardid, nodegroupid, name, graphid, config|
|**cards_x_nodes_x_widgets**|cardid, id, config, label, sortorder, nodeid, widgetid, visible|
|**concepts**|nodetype, conceptid, legacyoid|
|**constraints_x_nodes**|id, constraintid, nodeid|
|**d_data_types**|configcomponent, defaultconfig, configname, defaultwidget, isgeometric, issearchable, datatype, iconclass, modulename, classname|
|**d_languages**|isdefault, languageid, languagename|
|**d_node_types**|nodetype, namespace|
|**d_relation_types**|relationtype, namespace, category|
|**d_value_types**|namespace, category, valuetype, datatype, description|
|**django_admin_log**|change_message, id, action_time, object_id, object_repr, action_flag, content_type_id, user_id|
|**django_celery_results_taskresult**|id, task_id, status, content_type, content_encoding, result, date_done, traceback, meta, task_args, task_kwargs, task_name, worker, date_created|
|**django_content_type**|model, app_label, id|
|**django_migrations**|applied, id, app, name|
|**django_session**|expire_date, session_data, session_key|
|**edges**|name, edgeid, description, ontologyproperty, graphid, domainnodeid, rangenodeid|
|**edit_log**|oldprovisionalvalue, timestamp, userid, user_firstname, user_lastname, user_email, note, resourcedisplayname, user_username, newprovisionalvalue, oldvalue, provisional_edittype, provisional_user_username, provisional_userid, newvalue, edittype, tileinstanceid, nodegroupid, resourceinstanceid, resourceclassid, editlogid|
|**files**|path, fileid, tileid|
|**functions**|functiontype, functionid, component, classname, modulename, defaultconfig, description, name|
|**functions_x_graphs**|id, config, graphid, functionid|
|**geocoders**|name, component, geocoderid, api_key|
|**geojson_geometries**|resourceinstanceid, geom, tileid, id, nodeid|
|**graphs**|isresource, graphid, name, description, deploymentfile, author, deploymentdate, version, isactive, iconclass, subtitle, ontologyid, color, jsonldcontext, config, templateid, slug|
|**graphs_x_mapping_file**|mapping, graphid, id|
|**group_map_settings**|group_id, min_zoom, id, max_zoom, default_zoom|
|**guardian_groupobjectpermission**|object_pk, group_id, permission_id, id, content_type_id|
|**guardian_userobjectpermission**|object_pk, permission_id, user_id, id, content_type_id|
|**icons**|cssclass, id, name|
|**iiif_manifests**|label, manifest, description, id, url|
|**manifest_images**|image, imageid|
|**map_layers**|name, searchonly, icon, layerdefinitions, legend, zoom, centery, isoverlay, centerx, activated, addtomap, maplayerid|
|**map_markers**|id, name, url|
|**map_sources**|name, id, source|
|**mobile_surveys**|datadownloadconfig, tilecache, bounds, lasteditedby_id, createdby_id, description, enddate, name, onlinebasemaps, startdate, id, active|
|**mobile_surveys_x_cards**|card_id, mobile_survey_x_card_id, sortorder, mobile_survey_id|
|**mobile_surveys_x_groups**|mobile_survey_id, mobile_survey_x_group_id, group_id|
|**mobile_surveys_x_users**|user_id, mobile_survey_id, mobile_survey_x_user_id|
|**mobile_sync_log**|survey_id, status, userid, message, finished, started, logid|
|**node_groups**|nodegroupid, cardinality, parentnodegroupid, legacygroupid|
|**nodes**|isrequired, sortorder, fieldname, graphid, datatype, ontologyclass, exportable, nodeid, nodegroupid, issearchable, config, istopnode, description, name|
|**notification_types**|emailnotify, name, typeid, emailtemplate, webnotify|
|**notifications**|context, notiftype_id, id, created, message|
|**oauth2_provider_accesstoken**|expires, id, token, scope, application_id, user_id, created, updated, source_refresh_token_id|
|**oauth2_provider_application**|client_type, id, client_id, redirect_uris, updated, created, skip_authorization, user_id, name, client_secret, authorization_grant_type|
|**oauth2_provider_grant**|id, expires, redirect_uri, scope, updated, created, user_id, application_id, code|
|**oauth2_provider_refreshtoken**|id, created, user_id, revoked, application_id, access_token_id, token, updated|
|**ontologies**|name, version, path, parentontologyid, namespaces, ontologyid|
|**ontologyclasses**|ontologyid, target, source, ontologyclassid|
|**plugins**|icon, pluginid, sortorder, slug, config, componentname, component, name|
|**relations**|relationtype, relationid, conceptidto, conceptidfrom|
|**report_templates**|name, preload_resource_data, defaultconfig, componentname, component, description, templateid|
|**resource_2_resource_constraints**|resourceclassto, resourceclassfrom, resource2resourceid|
|**resource_instances**|graphid, createdtime, legacyid, resourceinstanceid|
|**resource_revision_log**|synctimestamp, resourceid, logid, synclog_id, survey_id, action, revisionid|
|**resource_x_resource**|resourcexid, resourceinstanceidto, modified, created, inverserelationshiptype, tileid, nodeid, resourceinstancefrom_graphid, resourceinstanceto_graphid, relationshiptype, dateended, datestarted, notes, resourceinstanceidfrom|
|**search_component**|enabled, sortorder, componentname, componentpath, type, classname, modulename, icon, name, searchcomponentid|
|**search_export_history**|exporttime, searchexportid, user_id, numberofinstances, url, downloadfile|
|**spatial_ref_sys**|proj4text, srtext, auth_srid, auth_name, srid|
|**tile_revision_log**|logid, survey_id, synctimestamp, revisionid, resourceid, tileid, synclog_id, action|
|**tiles**|nodegroupid, parenttileid, resourceinstanceid, provisionaledits, tileid, tiledata, sortorder|
|**user_profile**|id, phone, user_id|
|**user_x_notification_types**|notiftype_id, emailnotify, id, user_id, webnotify|
|**user_x_notifications**|isread, id, recipient_id, notif_id|
|**user_x_tasks**|user_id, taskid, status, datestart, datedone, name, id|
|**values**|valueid, value, conceptid, languageid, valuetype|
|**widgets**|widgetid, name, component, defaultconfig, helptext, datatype|
