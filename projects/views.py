import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .constants import (
    PROJECT_CLOSED_PARTICIPATION_ERROR,
    PROJECT_OWNER_PARTICIPATION_ERROR,
    PROJECT_SKILL_REQUIRED_ERROR,
    PROJECTS_PER_PAGE,
    SKILL_AUTOCOMPLETE_LIMIT,
)
from .forms import ProjectForm
from .models import Project, Skill


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = PROJECTS_PER_PAGE

    def get_queryset(self):
        queryset = Project.objects.select_related('owner').prefetch_related(
            'participants',
            'skills',
        )
        skill_name = self.request.GET.get('skill')
        if skill_name:
            queryset = queryset.filter(skills__name=skill_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()
        context['active_skill'] = self.request.GET.get('skill')
        context['query_prefix'] = (
            f"skill={context['active_skill']}&"
            if context['active_skill']
            else ''
        )
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'

    def get_queryset(self):
        return Project.objects.select_related('owner').prefetch_related(
            'participants',
            'skills',
        )


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'projects:detail',
            kwargs={'project_id': self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ProjectUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'
    pk_url_kwarg = 'project_id'

    def get_success_url(self):
        return reverse_lazy(
            'projects:detail',
            kwargs={'project_id': self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


@login_required
@require_POST
def join_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner != request.user and project.status == Project.Status.OPEN:
        project.participants.add(request.user)
    return redirect('projects:detail', project_id=project.pk)


@login_required
@require_POST
def close_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    project.status = Project.Status.CLOSED
    project.save(update_fields=['status'])
    return redirect('projects:detail', project_id=project.pk)


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    project.status = Project.Status.CLOSED
    project.save(update_fields=['status'])
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner == request.user:
        return JsonResponse(
            {
                'status': 'error',
                'error': PROJECT_OWNER_PARTICIPATION_ERROR,
            },
            status=HTTPStatus.BAD_REQUEST
        )
    if project.status != Project.Status.OPEN:
        return JsonResponse(
            {
                'status': 'error',
                'error': PROJECT_CLOSED_PARTICIPATION_ERROR,
            },
            status=HTTPStatus.BAD_REQUEST
        )
    is_participant = project.participants.filter(pk=request.user.pk).exists()
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({
        'status': 'ok',
        'participant': not is_participant,
    })


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    is_favorite = project.favorites.filter(pk=request.user.pk).exists()
    if is_favorite:
        project.favorites.remove(request.user)
    else:
        project.favorites.add(request.user)
    return JsonResponse({'is_favorite': not is_favorite})


class FavoriteProjectsView(LoginRequiredMixin, ListView):
    template_name = 'projects/favorite_projects.html'
    context_object_name = 'projects'
    paginate_by = PROJECTS_PER_PAGE

    def get_queryset(self):
        return self.request.user.favorites.select_related('owner').prefetch_related(
            'participants',
            'skills',
        )


@login_required
@require_POST
def add_project_skill(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    data = json.loads(request.body)
    skill_id = data.get('skill_id')
    skill_name = data.get('name', '').strip()
    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
        created = False
    elif skill_name:
        skill, created = Skill.objects.get_or_create(name=skill_name)
    else:
        return JsonResponse(
            {'error': PROJECT_SKILL_REQUIRED_ERROR},
            status=HTTPStatus.BAD_REQUEST
        )
    project.skills.add(skill)
    return JsonResponse({
        'id': skill.id,
        'name': skill.name,
        'created': created,
    })


@login_required
@require_POST
def remove_project_skill(request, project_id, skill_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    skill = get_object_or_404(Skill, pk=skill_id)
    project.skills.remove(skill)
    return JsonResponse({'success': True})


@login_required
def skill_autocomplete(request):
    query = request.GET.get('q', '').strip()
    skills = Skill.objects.filter(
        name__icontains=query
    )[:SKILL_AUTOCOMPLETE_LIMIT]
    return JsonResponse(
        [
            {'id': skill.id, 'name': skill.name}
            for skill in skills
        ],
        safe=False,
    )
