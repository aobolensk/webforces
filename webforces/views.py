from dataclasses import dataclass

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from loguru import logger

from webforces.server.core import Core
from webforces.server.structs import DBStatus, Algorithm
from webforces.settings import GIT_REPO_LINK
from webforces.forms import BuyAlgForm, NewAlgForm, UpdUserForm


@dataclass
class Href:
    id: str = ''
    url: str = ''
    description: str = ''


def get_indexes(user):
    if user.is_superuser:
        return [
            Href("StoreButton", "/store", "store"),
            Href("UserProfileButton", "/users/"+user.username+"/", "profile"),
            Href("StatisticsButton", "/stats/", "stats"),
            Href("ApiButton", "/api/", "api"),
            Href("SignOutButton", "/accounts/logout/", "sign out"),
        ]
    elif user.is_authenticated:
        return [
            Href("StoreButton", "/store", "store"),
            Href("UserProfileButton", "/users/"+user.username+"/", "profile"),
            Href("SignOutButton", "/accounts/logout/", "sign out"),
        ]
    return [
        Href("SignInButton", "/accounts/login/", "sign in"),
        Href("SignUpButton", "/accounts/sign_up/", "sign up"),
    ]


class MainPageView(TemplateView):
    template_name = "main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_index"] = get_indexes(self.request.user)
        context["git_repo_link"] = GIT_REPO_LINK
        return context


class UserView(MainPageView):
    template_name = "user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.kwargs['user']
        context["auth"] = self.request.user.is_authenticated
        core = Core()
        status, user = core.db.getUserByLogin(self.kwargs['user'])
        if status != DBStatus.s_ok:
            context["full_name"] = ""
        else:
            context["full_name"] = f"{user.first_name} {user.middle_name} {user.second_name}"
        return context


class UpdUserView(FormView):
    template_name = "user_update.html"
    form_class = UpdUserForm

    def get_success_url(self) -> str:
        return f'/users/{self.request.user.username}'

    def get_initial(self):
        core = Core()

        status, user = core.db.getUserByLogin(self.request.user.username)
        if status != DBStatus.s_ok:
            return {}

        initial = {
            "first_name": user.first_name,
            "second_name": user.second_name,
            "middle_name": user.middle_name,
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_index"] = get_indexes(self.request.user)
        context["git_repo_link"] = GIT_REPO_LINK
        return context

    def form_valid(self, form):
        core = Core()
        status, user = core.db.getUserByLogin(self.request.user.username)
        if status != DBStatus.s_ok:
            messages.error(self.request, "Internal error: can not find current user!")
            return super().form_valid(form)

        user.first_name = form.cleaned_data["first_name"]
        user.second_name = form.cleaned_data["second_name"]
        user.middle_name = form.cleaned_data["middle_name"]

        status = core.db.updFNUser(user)
        if status == DBStatus.s_ok:
            messages.info(self.request, 'User profile was successfully updated!')
        else:
            messages.error(self.request, "Internal error: can not update user profile!")

        return super().form_valid(form)


class StatsView(MainPageView):
    template_name = "stats.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        context = super().get_context_data(**kwargs)
        core = Core()
        status, stats = core.db.getStats()
        logger.warning(stats)
        if status != DBStatus.s_ok:
            logger.error("Could not get stats")
            raise Exception("Could not get stats")
        context["stats"] = stats.__dict__
        return context


@dataclass
class Algorithms_preview:
    alg_id: int = 0
    title: str = ''
    description: str = ''
    cost: int = 0
    available: bool = False


class StoreView(MainPageView):
    template_name = "store.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        core = Core()
        status, user = core.db.getUserByLogin(self.request.user.username)
        if status != DBStatus.s_ok:
            messages.error(self.request, "Internal error: can not find current user!")
            return context
        status, algorithms_list, available_list = core.db.getAllAvailableAlgs(user.user_id)
        if status != DBStatus.s_ok:
            messages.error(self.request, "Internal error: can not get list of algorithms!")
            return context
        algorithms_preview_list = []
        for i in range(len(algorithms_list)):
            algorithms_preview_list.append(Algorithms_preview(algorithms_list[i].alg_id,
                                           algorithms_list[i].title, algorithms_list[i].description,
                                           algorithms_list[i].cost, available_list[i]))
        context["algorithms_preview_list"] = algorithms_preview_list
        return context


class AddAlgView(FormView):
    template_name = "add_alg.html"
    form_class = NewAlgForm
    success_url = '/store'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_index"] = get_indexes(self.request.user)
        context["git_repo_link"] = GIT_REPO_LINK
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        core = Core()
        status, user = core.db.getUserByLogin(self.request.user.username)
        if status != DBStatus.s_ok:
            messages.error(self.request, "Internal error: can not find current user!")
            return super().form_valid(form)

        algorithm = Algorithm(0, title=form.cleaned_data['title'],
                              description=form.cleaned_data['description'],
                              author_id=user.user_id,
                              source=form.cleaned_data['source'],
                              cost=form.cleaned_data['cost']
                              )
        status, alg = core.db.addAlg(algorithm)
        if status == DBStatus.s_ok:
            messages.info(self.request, 'New algorithm was successfully added!')
        else:
            messages.error(self.request, "Internal error: can not add algorithm to database!")

        return super().form_valid(form)


class AlgView(MainPageView):
    template_name = "alg_page.html"


class BuyAlgView(FormView):
    template_name = "buy_alg.html"
    form_class = BuyAlgForm
    success_url = '/store'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_index"] = get_indexes(self.request.user)
        context["git_repo_link"] = GIT_REPO_LINK
        return context

    def form_valid(self, form):
        core = Core()
        status, user = core.db.getUserByLogin(self.request.user.username)
        if status != DBStatus.s_ok:
            messages.error(self.request, "Internal error: can not find current user!")
            return super().form_valid(form)

        user.bound_ids.append(self.kwargs["alg_id"])
        status = core.db.bindAlg(user)
        if status == DBStatus.s_ok:
            messages.info(self.request, 'New algorithm was successfully added!')
        else:
            messages.error(self.request, 'Internal error: can not buy algorithm!')
        return super().form_valid(form)


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
