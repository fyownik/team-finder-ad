from django.urls import path
from django.views.generic import RedirectView

from .views import (
    RegisterView,
    UserDetailView,
    UserListView,
    UserLoginView,
    UserPasswordChangeView,
    UserUpdateView,
    logout_user,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('list/', UserListView.as_view(), name='list'),
    path('edit-profile/', UserUpdateView.as_view(), name='edit_profile'),
    path(
        'change-password/',
        UserPasswordChangeView.as_view(),
        name='change_password'
    ),
    path(
        'None/',
        RedirectView.as_view(pattern_name='users:login', permanent=False)
    ),
    path('<int:user_id>/', UserDetailView.as_view(), name='profile'),
]
