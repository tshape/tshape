from django.conf.urls import include, url

from profiles.views import (ProfileCreateView, ProfileDetailView,
                            ProfileListView, ProfileUpdateView)


app_name = 'profiles'

urlpatterns = [
    url(r'^(?P<profile_id>\d+)/skillsets/', include('skillsets.urls')),
    url(r'^(?P<profile_id>\d+)/edit/$', ProfileUpdateView.as_view(), name='edit'),
    url(r'^(?P<profile_id>\d+)/$', ProfileDetailView.as_view(), name='detail'),
    url(r'^new/$', ProfileCreateView.as_view(), name='new'),
    url(r'^$', ProfileListView.as_view(), name='list'),
]
