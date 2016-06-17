from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'skillsets/javascript', views.skill, name='skill'),
    url(r'skillsets', views.skillsets, name='skillsets'),
    url(r'new', views.new, name='new'),
    url(r'^', views.index, name='index')
]
