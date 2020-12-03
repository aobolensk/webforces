from dataclasses import dataclass

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView

from webforces.server.core import Core
from webforces.server.structs import DBStatus


@dataclass
class Href:
    url: str = ''
    description: str = ''


class MainPageView(TemplateView):
    template_name = "main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_index"] = self.get_indexes(self.request.user)
        return context

    def get_indexes(self, user):
        if user.is_superuser:
            return [
                Href("/users/"+user.username+"/", "profile"),
                Href("/api/", "api"),
                Href("/accounts/logout/", "sign out"),
            ]
        elif user.is_authenticated:
            return [
                Href("/users/"+user.username+"/", "profile"),
                Href("/accounts/logout/", "sign out"),
            ]
        return [
            Href("/accounts/login/", "sign in"),
            Href("/accounts/sign_up/", "sign up"),
        ]


class UserView(MainPageView):
    template_name = "user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.kwargs['user']
        context["auth"] = self.request.user.is_authenticated
        core = Core()
        status, user = core.db.getUserByLogin(self.kwargs['user'])
        if status != DBStatus.s_ok:
            context["fullname"] = ""
        else:
            context["fullname"] = f"{user.first_name} {user.middle_name} {user.second_name}"
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
            Core().auth.register(username, raw_password)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                Core().auth.authenticate(username, password)
                return redirect(request.GET.get('next') or '/')
        else:
            messages.error(request, 'Incorrect username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
