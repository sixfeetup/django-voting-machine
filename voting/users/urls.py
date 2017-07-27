from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.HomePageView.as_view(),
        name='home'
    ),
    url(
        regex=r'^list$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
    url(
        regex=r'^~emailupdate/$',
        view=views.UserUpdateEmailView.as_view(),
        name='update_email'
    ),
    url(
        regex=r'^~passwordupdate/$',
        view=views.UserUpdatePasswordView.as_view(),
        name='update_password'
    ),
    # url(
    #     regex=r'^~passwordupdate/$',
    #     view=views.UserUpdateTeamView.as_view(),
    #     name='update_team'
    # ),
    url(
        regex=r'^signup/$',
        view=views.signup,
        name='signup'
    ),
    url(
        r'^login/$',
        auth_views.login,
        {'template_name':'users/login.html'},
        name='login'
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'template_name':'users/logout.html'},
        name='logout'
    ),
    url(
        regex=r'^create_team/$',
        view=views.create_team,
        name='create_team'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
]
