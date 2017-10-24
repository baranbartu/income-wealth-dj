import csv

from django import forms
from incomewealth.utils import read_csv


class CsvFileForm(forms.Form):
    csv_file = forms.FileField()

    # it will be automatically evaluated while checking validity
    def clean_csv_file(self):
        f = self.cleaned_data['csv_file']

        if f.content_type not in ['text/csv']:
            raise forms.ValidationError('The file type is not accepted.')

        try:
            data = read_csv(f) # noqa
        except csv.Error:
            raise forms.ValidationError('The file is broken or not csv.')

        return f
