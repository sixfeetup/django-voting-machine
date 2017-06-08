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
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
    # url(
    #     regex=r'^account_activation_sent/$',
    #     view=core_views.account_activation_sent,
    #     name='account_activation_sent'
    # ),
    # url(
    #     regex=r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     view=core_views.activate,
    #     name='activate'
    # ),
    #
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     core_views.activate, name='activate'
#    ),
]
