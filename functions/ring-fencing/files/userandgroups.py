from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.models import User, Group

# /get/users
class getUsers(View):
	
	def get(self, request):

		#groups = [{"name":group.name, "id":group.id, "type": "group"} for group in Group.objects.all()]
		users = [{"name":user.username, "id":user.id, "type": "user"} for user in User.objects.all()]

		return JsonResponse(users, safe=False)

