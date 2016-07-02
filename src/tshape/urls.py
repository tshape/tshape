"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_nested import routers

from profiles import views as profile_views
from skills import views as skill_views
from skillsets import views as skillset_views
from tshape.views import IndexView
from users import views as user_views


# Create a router and register our viewsets with it.
router = routers.SimpleRouter()
router.register(r'profiles', profile_views.ProfileViewSet)
router.register(r'skills', skill_views.SkillViewSet)
router.register(r'skillsets', skillset_views.SkillsetViewSet)
router.register(r'users', user_views.UserViewSet)

skillsets_router = routers.NestedSimpleRouter(
    router, r'skillsets', lookup='skillset')
skillsets_router.register(r'skills', skill_views.SkillViewSet)

profiles_router = routers.NestedSimpleRouter(
    router, r'profiles', lookup='profile')
profiles_router.register(r'skills', skill_views.SkillViewSet)
profiles_router.register(r'skillsets', skillset_views.SkillsetViewSet)

profile_skillsets_router = routers.NestedSimpleRouter(
    profiles_router, r'skillsets', lookup='skillset')
profile_skillsets_router.register(r'skills', skill_views.SkillViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    # api routes
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(skillsets_router.urls)),
    url(r'^api/', include(profiles_router.urls)),
    url(r'^api/', include(profile_skillsets_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # regular routes
    url(r'^profile/', include('profiles.urls'), name='profiles'),
    url(r'^skillsets/', include('skillsets.urls'), name='skillsets'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', user_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', user_views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', user_views.SignupView.as_view(), name='signup'),
    url(r'^$', IndexView.as_view(), name='index'),
]
