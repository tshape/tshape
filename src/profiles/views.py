from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets

from profiles.forms import ProfileForm
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from tshape.utils import PKContextMixin


class ProfileCreateView(CreateView):

    form_class = ProfileForm
    template_name = 'profiles/new.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if hasattr(user, 'profile'):
            return HttpResponseRedirect(
                reverse('profiles:detail', kwargs={'profile_id': user.id}))
        return super(ProfileCreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return reverse('profiles:detail',
                       kwargs={'profile_id': profile.user_id})


class ProfileDetailView(PKContextMixin, DetailView):

    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, profile_id, *args, **kwargs):
        # profile_id = self.kwargs.get('profile_id')
        # if profile_id:
        return Profile.objects.get(pk=profile_id)
        # return None


class ProfileListView(ListView):

    model = Profile
    template_name = 'profiles/list.html'


class ProfileUpdateView(PKContextMixin, UpdateView):

    form_class = ProfileForm
    template_name = 'profiles/edit.html'

    def get_object(self, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        return Profile.objects.get(pk=profile_id)

    def form_valid(self, form, *args, **kwargs):
        profile = form.save()
        return reverse('profiles:detail',
                       kwargs={'profile_id': profile.user_id})


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
