from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import re

# Import the corrected and updated functions from your other modules
from .zip_file import save_zip, clean_up_files
from .zenodo_publish import zenodo_publish
from .zenodo_calculate import zenodo_contributors, zenodo_keywords, zenodo_dates, add_alternative_name
from .forms import CitationForm
from .zenodo import zenodo_map, zenodo_statistics_hp

def text_to_filename(text):
    """Cleans a string to make it suitable for use as a filename."""
    filename = text.replace(' ', '_').lower()
    filename = re.sub(r'[^\w-]', '', filename)
    return filename

def citation_generator(request):
    """
    Handles the form submission, data processing, and Zenodo publication.
    This view is updated to only handle pasted JSON text.
    """
    if request.method == 'POST':
        form = CitationForm(request.POST)
        if form.is_valid():
            # --- Get Data from Form ---
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            advanced = form.cleaned_data['advanced']

            # --- Get Zenodo Config from Django Settings ---
            zenodo_url = getattr(settings, 'ZENODO_URL', "https://zenodo.org/api/deposit/depositions")
            token = getattr(settings, 'ZENODO_ACCESS_TOKEN', None)

            if not token:
                return HttpResponse("Error: ZENODO_ACCESS_TOKEN not configured in Django settings.")

            # --- Load Data from Pasted Text ---
            data = {}
            try:
                data = json.loads(form.cleaned_data['json_text'])
            except json.JSONDecodeError:
                return HttpResponse("Error: The pasted text is not valid JSON.")

            # --- Process Data ---
            filename = text_to_filename(title)
            
            data = add_alternative_name(data)

            plot_filenames = []
            if advanced:
                print("Advanced option selected. Generating plots and maps...")
                plot_filenames = [
                    f"{filename}_map_local.png", f"{filename}_map_national.png",
                    f"{filename}_map_eamena_scope.png", f"{filename}_stat_hp_conditions.png",
                    f"{filename}_stat_hp_functions.png"
                ]
                zenodo_map(filename, data)
                zenodo_statistics_hp(filename, data)

            save_zip(data, filename, plot_filenames)

            # --- Calculate Metadata ---
            print("Calculating metadata fields for Zenodo...")
            zenodo_calculated_fields = (
                zenodo_contributors(data),
                zenodo_keywords(data),
                zenodo_dates(data)
            )
            print("Metadata calculation complete.")

            # --- Publish to Zenodo ---
            r = zenodo_publish(title, filename, description, zenodo_calculated_fields, zenodo_url, token)
            
            # --- Clean Up and Respond ---
            clean_up_files(filename, plot_filenames)
            
            if r:
                return HttpResponse(f"Success! Dataset published. View it here: <a href='{r}' target='_blank'>{r}</a>")
            else:
                return HttpResponse("Publication failed. Please check the console logs for errors.")
    else:
        form = CitationForm()

    return render(request, 'citation_form.html', {'form': form})
