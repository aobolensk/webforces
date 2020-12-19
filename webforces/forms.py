from django import forms


class NewAlgForm(forms.Form):
    title = forms.CharField(max_length=100, label="",
                            widget=forms.TextInput(attrs={'id': 'NewAlgTitle', 'placeholder': 'Title'}))
    description = forms.CharField(label="",
                                  widget=forms.Textarea(attrs={'id': 'NewAlgDescription',
                                                               'placeholder': 'Description'}))
    cost = forms.FloatField(min_value=0, label="",
                            widget=forms.TextInput(attrs={'id': 'NewAlgCost', 'placeholder': 'Cost'}))
    source = forms.CharField(label="",
                             widget=forms.Textarea(attrs={'id': 'NewAlgSource', 'placeholder': 'Source'}))
