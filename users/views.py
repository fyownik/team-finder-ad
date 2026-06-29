from django.contrib.auth import logout
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import UserLoginForm, UserPasswordChangeForm, UserProfileForm, UserRegisterForm
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


class UserLogoutView(LoginRequiredMixin, View):
    next_page = reverse_lazy('projects:list')

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.next_page)

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.next_page)


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.owned_projects.all()
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'users'
    paginate_by = 12

    def get_queryset(self):
        queryset = User.objects.all()
        if not self.request.user.is_authenticated:
            return queryset
        active_filter = self.request.GET.get('filter')
        if active_filter == 'owners-of-favorite-projects':
            queryset = User.objects.filter(
                owned_projects__favorites=self.request.user
            )
        elif active_filter == 'owners-of-participating-projects':
            queryset = User.objects.filter(
                owned_projects__participants=self.request.user
            )
        elif active_filter == 'interested-in-my-projects':
            queryset = User.objects.filter(
                favorites__owner=self.request.user
            )
        elif active_filter == 'participants-of-my-projects':
            queryset = User.objects.filter(
                joined_projects__owner=self.request.user
            )
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_filter = self.request.GET.get('filter')
        context['active_filter'] = active_filter
        context['query_prefix'] = f'filter={active_filter}&' if active_filter else ''
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})
