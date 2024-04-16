from django import forms

class CitationForm(forms.Form):
    geojson_url = forms.CharField(max_length=1000, label="Geojson URL", widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
    title = forms.CharField(max_length=1000, label="Title")
    description = forms.CharField(max_length=1000, label="Description", widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))