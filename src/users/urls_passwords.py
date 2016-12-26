from django.conf.urls import url

from users.views import UserPasswordViews


app_name = 'passwords'

urlpatterns = [
    url(r'^change_password/$', UserPasswordViews.change_password,
        name='change_password'),
    url(r'^reset_password/done/$', UserPasswordViews.reset_password_done,
        name='reset_password_done'),
    url(r'^reset_password/$', UserPasswordViews.reset_password,
        name='reset_password'),
    url(r'^reset_confirm/done/$', UserPasswordViews.reset_confirm_done,
        name='reset_confirm_done'),
    url(r'^reset_confirm/(?P<uidb36>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        UserPasswordViews.reset_confirm, name='reset_confirm'),
]
