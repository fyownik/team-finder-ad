import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ProjectForm
from .models import Project, Skill


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

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
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

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

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


class JoinProjectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.owner != request.user and project.status == Project.Status.OPEN:
            project.participants.add(request.user)
        return redirect('projects:detail', pk=project.pk)


class CloseProjectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        project.status = Project.Status.CLOSED
        project.save(update_fields=['status'])
        return redirect('projects:detail', pk=project.pk)


class CompleteProjectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        project.status = Project.Status.CLOSED
        project.save(update_fields=['status'])
        return JsonResponse({'status': 'ok'})


class ToggleParticipateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.owner == request.user or project.status != Project.Status.OPEN:
            return JsonResponse({'status': 'error'}, status=400)
        if request.user in project.participants.all():
            project.participants.remove(request.user)
            is_participant = False
        else:
            project.participants.add(request.user)
            is_participant = True
        return JsonResponse({
            'status': 'ok',
            'participant': is_participant,
        })


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if request.user in project.favorites.all():
            project.favorites.remove(request.user)
            is_favorite = False
        else:
            project.favorites.add(request.user)
            is_favorite = True
        return JsonResponse({'is_favorite': is_favorite})


class FavoriteProjectsView(LoginRequiredMixin, ListView):
    template_name = 'projects/favorite_projects.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        return self.request.user.favorites.select_related('owner').prefetch_related(
            'participants',
            'skills',
        )


class AddProjectSkillView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        data = json.loads(request.body)
        skill_id = data.get('skill_id')
        skill_name = data.get('name', '').strip()
        if skill_id:
            skill = get_object_or_404(Skill, pk=skill_id)
            created = False
        elif skill_name:
            skill, created = Skill.objects.get_or_create(name=skill_name)
        else:
            return JsonResponse({'error': 'Название навыка обязательно'}, status=400)
        project.skills.add(skill)
        return JsonResponse({
            'id': skill.id,
            'name': skill.name,
            'created': created,
        })


class RemoveProjectSkillView(LoginRequiredMixin, View):
    def post(self, request, pk, skill_id):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        skill = get_object_or_404(Skill, pk=skill_id)
        project.skills.remove(skill)
        return JsonResponse({'success': True})


class SkillAutocompleteView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        skills = Skill.objects.filter(name__icontains=query)[:10]
        return JsonResponse(
            [
                {'id': skill.id, 'name': skill.name}
                for skill in skills
            ],
            safe=False,
        )
