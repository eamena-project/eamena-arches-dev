from django import forms

class CitationForm(forms.Form):
    """
    This form is updated with CSS classes in the widgets to allow for
    beautiful styling with Tailwind CSS in the template.
    """
    # --- Data Input Field ---
    json_text = forms.CharField(
        label="Paste GeoJSON Content",
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow duration-300 ease-in-out',
            'rows': 12,
            'placeholder': 'Paste the entire content of your GeoJSON file here...'
        })
    )

    # --- Metadata Fields ---
    title = forms.CharField(
        label="Title",
        max_length=1000,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow duration-300 ease-in-out',
            'placeholder': 'The title for the Zenodo dataset'
        })
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-shadow duration-300 ease-in-out',
            'rows': 3,
            'placeholder': 'A brief description for the Zenodo dataset'
        })
    )
    advanced = forms.BooleanField(
        label="Generate Advanced Outputs (Maps & Plots)",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-5 w-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
        })
    )
