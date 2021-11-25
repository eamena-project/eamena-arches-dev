from arches.app.models.resource import Resource
for id in non_jordan_resource_ids:
    r = Resource.objects.get(pk=id)
    r.delete()