from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets

from profiles.forms import ProfileForm
from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfileDetailView(DetailView):

    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        if profile_id:
            return Profile.objects.get(pk=profile_id)
        return self.request.user.profile


class ProfileListView(ListView):

    model = Profile
    template_name = 'profiles/list.html'


class ProfileUpdateView(UpdateView):

    form_class = ProfileForm
    template_name = 'profiles/edit.html'

    def get_object(self, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        return Profile.objects.get(pk=profile_id)

    def form_valid(self, form, *args, **kwargs):
        form.save()
        return super(ProfileUpdateView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('profiles:detail',
                       kwargs={'profile_id': self.request.user.id})


class ProfileViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]
