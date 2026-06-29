from django.urls import path

from .views import *

app_name = 'projects'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='list'),
    path('favorites/', FavoriteProjectsView.as_view(), name='favorites'),
    path('create-project/', ProjectCreateView.as_view(), name='create'),
    path('skills/', SkillAutocompleteView.as_view(), name='skill_list'),
    path('skills/autocomplete/', SkillAutocompleteView.as_view(), name='skill_autocomplete'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='edit'),
    path('<int:pk>/join/', JoinProjectView.as_view(), name='join'),
    path('<int:pk>/close/', CloseProjectView.as_view(), name='close'),
    path('<int:pk>/complete/', CompleteProjectView.as_view(), name='complete'),
    path(
        '<int:pk>/toggle-participate/', 
        ToggleParticipateView.as_view(), 
        name='toggle_participate'
    ),
    path('<int:pk>/toggle-favorite/', ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('<int:pk>/skills/add/', AddProjectSkillView.as_view(), name='add_skill'),
    path(
        '<int:pk>/skills/<int:skill_id>/remove/', 
        RemoveProjectSkillView.as_view(), 
        name='remove_skill'
    ),
]
