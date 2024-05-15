from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.management import call_command
from django.middleware.csrf import get_token
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from arches.app.models.models import GraphModel
# from eamena.tasks import import_processed_bulk_upload_and_notify

import os, sys, json, uuid, datetime
import arches.app.utils.task_management as task_management

def __user_canbulkupload(user):

	ret = user.user_permissions.filter(codename='add_resourceinstance').count() + user.groups.filter(permissions__codename='add_resourceinstance').count()
	if ret == 0:
		return False
	return True

def index(request):

	if not(request.user.is_authenticated):
		return redirect('/auth/?next=/bulk-upload')

	if not(__user_canbulkupload(request.user)):
		return redirect('/auth/?next=/bulk-upload')

	return redirect('plugins/bulk-upload')

def handle_uploaded_file(f, upload_id, info={}):
	dest_path = os.path.join(settings.BULK_UPLOAD_DIR, upload_id)
	dest_file = os.path.join(settings.BULK_UPLOAD_DIR, upload_id, str(f))
	info_file = os.path.join(settings.BULK_UPLOAD_DIR, upload_id, 'info.json')
	errors_path = os.path.join(dest_path, 'error_reports')
	imports_path = os.path.join(dest_path, 'for_import')
	summary_path = os.path.join(dest_path, 'summary')
	os.makedirs(dest_path)
	os.makedirs(errors_path)
	os.makedirs(imports_path)
	os.makedirs(summary_path)
	with open(dest_file, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	with open(info_file, 'w') as fp:
		if 'filepath' in info:
			info['filepath'] = dest_path
		fp.write(json.dumps(info))
	return dest_file.replace(settings.BULK_UPLOAD_DIR, '')

def get_archesfile_path(filepath):
	basename = os.path.splitext(os.path.basename(filepath))[0].replace(' ', '_')
	name = time.strftime("{}_%Y%m%d%H%M%S.arches".format(basename))
	dest_path = os.path.join(settings.BULK_UPLOAD_DIR, name)
	return dest_path

def download_template(request, graphid):

	if not(request.user.is_authenticated):
		raise PermissionDenied

	if not(__user_canbulkupload(request.user)):
		raise PermissionDenied

	try:
		g = GraphModel.objects.get(graphid=str(graphid))
	except:
		raise Http404("Unknown resource model")
	template_file = os.path.join(settings.BULK_UPLOAD_TEMPLATE_DIR, str(graphid) + '.xlsx')
	download_file = str(g.name) + ' BUS Template.xlsx'
	if os.path.exists(template_file):
		with open(template_file, 'rb') as fp:
			file_data = fp.read()
		resp = HttpResponse(file_data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
		resp['Content-Disposition'] = 'attachment; filename="' + download_file + '"'
		return resp
	else:
		raise Http404(str(template_file) + ' not found')

def upload_spreadsheet(request):

	if request.method != 'POST':
		raise Http404()

	if not(request.user.is_authenticated):
		raise PermissionDenied

	if not(__user_canbulkupload(request.user)):
		raise PermissionDenied

	upload_id = str(datetime.datetime.now().strftime("%Y-%m-%d-")) + str(uuid.uuid4())
	f = request._files['files[]']
	fname = os.path.basename(str(f))
	response_data = {
		'filevalid': True,
		'filename': fname,
		'filepath': '',
		'upload': '',
		'user': {'id': request.user.id, 'name': request.user.get_username()},
		'csrf': get_token(request)
	}
	if request.user.email:
		response_data['user']['email'] = request.user.email
	if not fname.endswith('.xlsx'):
		response_data['filevalid'] = False
	else:
		fpath = handle_uploaded_file(f, upload_id, response_data)
		response_data['filepath'] = os.path.dirname(fpath)
		response_data['upload'] = upload_id

	return HttpResponse(json.dumps(response_data), content_type="application/json")

def validate(request):

	if request.method != 'POST':
		raise Http404()

	if not(request.user.is_authenticated):
		raise PermissionDenied

	if not(__user_canbulkupload(request.user)):
		raise PermissionDenied

	upload_id = str(request.POST.get('uploadid', ''))
	graph_id = str(request.POST.get('graphid', ''))
	append_mode = str(request.POST.get('append', 'no'))
	filepath = os.path.join(settings.BULK_UPLOAD_DIR, upload_id)
	importfile = ''
	for file in os.scandir(filepath):
		if file.name.endswith('.xlsx'):
			importfile = file
	fullpath = os.path.join(filepath, importfile.name)
	errorpath = os.path.join(filepath, 'error_reports')

	response_data = []
	try:
		if append_mode == 'yes':
			call_command('bu', operation='validate', append='append', warnings='strict', source=fullpath, dest_dir=errorpath, graph=graph_id)
		else:
			call_command('bu', operation='validate', warnings='strict', source=fullpath, dest_dir=errorpath, graph=graph_id)
	except:
		response_data.append(['', 'Failed to validate file ' + str(importfile.name), 'Please check that you are uploading a valid Excel spreadsheet, formatted according to the appropriate Bulk Upload Sheet template.'])
	if len(response_data) == 0:
		validfile = ''
		for file in os.scandir(errorpath):
			if file.name.endswith('.json'):
				validfile = file
		fp = open(validfile, 'r')
		response_data = json.loads('\n'.join(fp.readlines()))
		fp.close()

	return HttpResponse(json.dumps(response_data), content_type="application/json")

def convert(request):

	if request.method != 'POST':
		raise Http404()

	if not(request.user.is_authenticated):
		raise PermissionDenied

	if not(__user_canbulkupload(request.user)):
		raise PermissionDenied

	upload_id = str(request.POST.get('uploadid', ''))
	graph_id = str(request.POST.get('graphid', ''))
	filepath = os.path.join(settings.BULK_UPLOAD_DIR, upload_id)
	importfile = ''
	infofile = ''
	info = {}
	for file in os.scandir(filepath):
		if file.name.endswith('.xlsx'):
			importfile = file
		if file.name.endswith('.json'):
			infofile = file
	fullpath = os.path.join(filepath, importfile.name)
	errorpath = os.path.join(filepath, 'error_reports')
	outputpath = os.path.join(filepath, 'for_import')
	with open(infofile, 'r') as fp:
		info = json.load(fp)

	response_data = {'success': False, 'errors': [], 'notification': None}
	try:
		user = User.objects.get(id=info['user']['id'])
	except:
		user = None
	if not(user is None):
		response_data['notification'] = user.email

	try:
		call_command('bu', operation='convert', warnings='strict', source=fullpath, dest_dir=outputpath, graph=graph_id)
		response_data['success'] = True
	except:
		response_data['errors'].append(['', 'Failed to validate file ' + str(importfile.name), 'Please check that you are uploading a valid Excel spreadsheet, formatted according to the appropriate Bulk Upload Sheet template.'])

	# if response_data['success']:
	# 	email = None
	# 	if 'user' in info:
	# 		if 'email' in info['user']:
	# 			email = info['user']['email']
	# 	import_processed_bulk_upload_and_notify.delay(notify_address=email, upload_path=filepath)

	return HttpResponse(json.dumps(response_data), content_type="application/json")

