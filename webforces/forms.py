from django import forms


class NewAlgForm(forms.Form):
    title = forms.CharField(max_length=100, label="",
                            widget=forms.TextInput(attrs={'id': 'NewAlgTitle'}))
    description = forms.CharField(label="",
                                  widget=forms.Textarea(attrs={'id': 'NewAlgDescription'}))
    source = forms.CharField(label="",
                             widget=forms.Textarea(attrs={'id': 'NewAlgSource'}))
