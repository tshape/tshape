from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from skillsets.views import (SkillsetCreateView, SkillsetDetailView,
                             SkillsetListView, SkillsetUpdateView,
                             MultipleSkillsetsUpdateView)


app_name = 'skillsets'

urlpatterns = [
    url(r'^skills/', include('skills.urls')),
    url(r'^new/$', SkillsetCreateView.as_view(), name='new'),
    url(r'^edit/$',
        MultipleSkillsetsUpdateView.as_view(), name='edit-all'),
    url(r'^(?P<skillset_id>\d+)/edit/$',
        SkillsetUpdateView.as_view(), name='edit'),
    url(r'^(?P<skillset_id>\d+)/$',
        SkillsetDetailView.as_view(), name='detail'),
    url(r'^$', SkillsetListView.as_view(), name='list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
