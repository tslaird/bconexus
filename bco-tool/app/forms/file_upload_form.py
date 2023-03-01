from django import forms


class FileUploadForm(forms.Form):
    file_choices = [('CWL', 'CWL'),('WDL', 'WDL'),('DNANexus', 'DNANexus')]
    file = forms.FileField(allow_empty_file=False, label = "Select File")
    file_type = forms.ChoiceField(choices=file_choices)
