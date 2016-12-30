from django.conf.urls import include, url

from users.views import UserDetailView, UserUpdateView


app_name = 'users'

urlpatterns = [
    url(r'^skillsets/', include('skillsets.urls'), name='skillsets'),
    url(r'^profile/edit/$',
        UserUpdateView.as_view(), name='edit'),
    url(r'^profile/$', UserDetailView.as_view(), name='detail'),
    url(r'^$', include('profiles.urls'), name='profiles'),
    # url(r'^$', UserListView.as_view(), name='list'),
]
