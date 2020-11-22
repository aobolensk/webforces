from dataclasses import dataclass

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

@dataclass
class Href:
    url: str = ''
    description: str = ''

class MainPageView(TemplateView):
    template_name = "base.html"

    _index = [
        Href("/accounts/sign_in/", "sign in"),
        Href("/accounts/sign_up/", "sign up"),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index'] = self._index
        return context

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
