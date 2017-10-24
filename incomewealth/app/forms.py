import csv
import copy

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
            # try was parsed or not, use deepcopy to keep original stream
            next(read_csv(copy.deepcopy(f)))
        except csv.Error:
            raise forms.ValidationError('The file is broken or not csv.')

        return f
