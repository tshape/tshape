from django.conf.urls import url

from profiles.views import ProfileDetailView, ProfileUpdateView


app_name = 'profiles'

urlpatterns = [
    url(r'^edit/$',
        ProfileUpdateView.as_view(), name='edit'),
    url(r'^$', ProfileDetailView.as_view(), name='detail'),
    # url(r'^$', ProfileListView.as_view(), name='list'),
]
