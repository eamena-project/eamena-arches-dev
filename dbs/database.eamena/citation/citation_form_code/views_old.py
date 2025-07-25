from django.http import HttpResponse
from django.shortcuts import render
import requests

from .zip_file import save_zip, clean_up_zip
from .zenodo_publish import zenodo_publish
from .zenodo_calculate import zenodo_contributors, zenodo_keywords, zenodo_dates
from .forms import CitationForm

import requests
import re, os

def text_to_filename(text):
	# Replace spaces with underscores
	filename = text.replace(' ', '_').lower()
	# Remove any punctuation using regular expressions
	filename = re.sub(r'[^\w\s]', '', filename)
	return filename

def citation_generator(request):
	if request.method == 'POST':
		form = CitationForm(request.POST)
		if form.is_valid():
			geojson_url = form.cleaned_data['geojson_url']
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			filename=text_to_filename(title)
			data = requests.get(geojson_url).json()
			save_zip(data, filename)
			zenodo_calculated_fields = zenodo_contributors(data), zenodo_keywords(data, additional=[]), zenodo_dates(data)
			r = zenodo_publish(title, filename, description, zenodo_calculated_fields)
			clean_up_zip(filename)
			return HttpResponse(f"Success! {r}")  # Redirect to a success page
	else:
		form = CitationForm()
	return render(request, "citation_form.html", {'form':form})
