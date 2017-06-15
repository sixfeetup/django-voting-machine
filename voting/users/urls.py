from django.conf.urls import url

from . import views
from . import views as core_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^signup/$',
        view=core_views.signup,
        name='signup'
    ),
    url(
        r'^login/$',
        auth_views.login,
        {'template_name':'users/login.html'},
        name='login'
    ),
    url(
        regex=r'^logout/$',
        view=core_views.logout_view,
        name='logout'
    ),
    url(
        regex=r'^create_team/$',
        view=core_views.create_team,
        name='create_team'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
]
