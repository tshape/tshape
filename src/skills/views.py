from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets

from skills.forms import SkillForm
from skills.models import Skill
from skills.serializers import SkillSerializer


class SkillCreateView(CreateView):

    form_class = SkillForm
    template_name = 'skills/new.html'

    def form_valid(self, form, *args, **kwargs):
        skill = form.save(commit=False)
        skill.user = self.request.user
        skill.save()
        return reverse('skills:detail', kwargs={'pk': skill.id})


class SkillDetailView(DetailView):

    model = Skill
    template_name = 'skills/detail.html'


class SkillListView(ListView):

    model = Skill
    template_name = 'skills/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SkillListView, self).get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        # profile_id = self.kwargs.get('profile_id')
        # skillset_id = self.kwargs.get('skillset_id')
        # skillsets = Profile.objects.get(pk=profile_id).skillsets()
        # skills = [skill for skill in skillsets if skillset.id == skillset_id]
        context['object_list'] = Skills.objects.filter(skillset_id=self.kwar)
        return context


class SkillUpdateView(UpdateView):

    form_class = SkillForm
    template_name = 'skills/edit.html'

    def form_valid(self, form, *args, **kwargs):
        skill = form.save()
        return reverse('skills:detail', kwargs={'pk': skill.id})


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
