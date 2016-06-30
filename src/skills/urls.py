from django.conf.urls import url

from skills.views import (SkillCreateView, SkillDetailView,
                          SkillListView, SkillUpdateView)


app_name = 'skills'

urlpatterns = [
    url(r'^new/$', SkillCreateView.as_view(), name='new'),
    url(r'^(?P<skill_id>\d+)/edit/$', SkillUpdateView.as_view(), name='edit'),
    url(r'^(?P<skill_id>\d+)/$', SkillDetailView.as_view(), name='detail'),
    url(r'^$', SkillListView.as_view(), name='list'),
]
