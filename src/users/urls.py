from django.conf.urls import url

from users.views import UserDetailView, UserUpdateView


app_name = 'users'

urlpatterns = [
    url(r'^(?P<user_id>\d+)/edit/$',
        UserUpdateView.as_view(), name='edit'),
    url(r'^(?P<user_id>\d+)/$', UserDetailView.as_view(), name='detail'),
    # url(r'^$', UserListView.as_view(), name='list'),
]
