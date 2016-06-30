from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from skillsets.views import (SkillsetCreateView, SkillsetDetailView,
                             SkillsetListView, SkillsetUpdateView)
                             # ProfileSkillsetsUpdateView)


app_name = 'skillsets'

urlpatterns = [
    url(r'^skills/', include('skills.urls')),
    url(r'^new/$', SkillsetCreateView.as_view(), name='new'),
    # url(r'^edit/$',
    #     ProfileSkillsetsUpdateView.as_view(), name='edit-all'),
    url(r'^(?P<skillset_id>\d+)/edit/$',
        SkillsetUpdateView.as_view(), name='edit'),
    url(r'^(?P<skillset_id>\d+)/$',
        SkillsetDetailView.as_view(), name='detail'),
    url(r'^$', SkillsetListView.as_view(), name='list'),
    # url(r'^skillsets/$', views.snippet_list),
    # url(r'^skillsets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
