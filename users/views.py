from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .constants import (
    ACTIVE_FILTER_CONTEXT_KEY,
    QUERY_PREFIX_CONTEXT_KEY,
    USER_FILTER_LOOKUPS,
    USER_FILTER_QUERY_PARAM,
    USER_ID_URL_KWARG,
    USER_PROJECTS_CONTEXT_KEY,
    USERS_PER_PAGE,
)
from .forms import UserLoginForm, UserProfileForm, UserRegisterForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('projects:list')


@login_required
def logout_user(request):
    logout(request)
    return redirect('projects:list')


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'
    pk_url_kwarg = USER_ID_URL_KWARG

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[USER_PROJECTS_CONTEXT_KEY] = self.object.owned_projects.all()
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={USER_ID_URL_KWARG: self.request.user.pk}
        )


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'users'
    paginate_by = USERS_PER_PAGE

    def get_queryset(self):
        queryset = User.objects.all()
        if not self.request.user.is_authenticated:
            return queryset
        active_filter = self.request.GET.get(USER_FILTER_QUERY_PARAM)
        filter_lookup = USER_FILTER_LOOKUPS.get(active_filter)
        if filter_lookup:
            queryset = User.objects.filter(
                **{filter_lookup: self.request.user}
            )
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_filter = self.request.GET.get(USER_FILTER_QUERY_PARAM)
        context[ACTIVE_FILTER_CONTEXT_KEY] = active_filter
        context[QUERY_PREFIX_CONTEXT_KEY] = (
            f'{USER_FILTER_QUERY_PARAM}={active_filter}&'
            if active_filter
            else ''
        )
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse_lazy(
            'users:profile',
            kwargs={USER_ID_URL_KWARG: self.request.user.pk}
        )
