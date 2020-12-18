from django import forms


class NewAlgForm(forms.Form):
    name = forms.CharField(max_length=100, label="",
                           widget=forms.TextInput(attrs={'id': 'new_alg_name'}))
    description = forms.CharField(max_length=100, label="",
                                  widget=forms.TextInput(attrs={'id': 'new_alg_description'}))
    code = forms.CharField(max_length=100, label="",
                           widget=forms.Textarea(attrs={'id': 'new_alg_code'}))

    def checkForm(self):
        pass
