from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('list/', UserListView.as_view(), name='list'),
    path('edit-profile/', UserUpdateView.as_view(), name='edit_profile'),
    path('change-password/', UserPasswordChangeView.as_view(), name='change_password'),
    path('<int:pk>/', UserDetailView.as_view(), name='profile'),
]
