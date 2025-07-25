from django.test import RequestFactory
from arches.app.views.api import SearchExport
import json, requests

def local_api_search(url, user):
	"""Uses the RequestFactory from Django's test framework to make a local call to the Arches API. This ensures all HTTP
	traffic is kept local, ensures a logged in user, and prevents any cross-site nonsense, making it more secure than
	simply doing an HTTP call."""

	rf = RequestFactory()
	view = SearchExport.as_view()
	r = rf.get(url)
	r.user = user

	try:
		ret = json.loads(view(r).content)
	except:
		ret = {}

	if len(ret) == 0:
		r = requests.get(url)
		ret = r.json()

	return ret
