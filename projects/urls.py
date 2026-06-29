from django.urls import path

from .views import (
    FavoriteProjectsView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    add_project_skill,
    close_project,
    complete_project,
    join_project,
    remove_project_skill,
    skill_autocomplete,
    toggle_favorite,
    toggle_participate,
)

app_name = 'projects'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='list'),
    path('favorites/', FavoriteProjectsView.as_view(), name='favorites'),
    path('create-project/', ProjectCreateView.as_view(), name='create'),
    path('skills/', skill_autocomplete, name='skill_list'),
    path('skills/autocomplete/', skill_autocomplete, name='skill_autocomplete'),
    path('<int:project_id>/', ProjectDetailView.as_view(), name='detail'),
    path('<int:project_id>/edit/', ProjectUpdateView.as_view(), name='edit'),
    path('<int:project_id>/join/', join_project, name='join'),
    path('<int:project_id>/close/', close_project, name='close'),
    path('<int:project_id>/complete/', complete_project, name='complete'),
    path(
        '<int:project_id>/toggle-participate/',
        toggle_participate,
        name='toggle_participate'
    ),
    path(
        '<int:project_id>/toggle-favorite/',
        toggle_favorite,
        name='toggle_favorite'
    ),
    path(
        '<int:project_id>/skills/add/',
        add_project_skill,
        name='add_skill'
    ),
    path(
        '<int:project_id>/skills/<int:skill_id>/remove/',
        remove_project_skill,
        name='remove_skill'
    ),
]
