from django.conf.urls import url

from . import views

app_name = 'votingmachine'
urlpatterns = [
    url(
        regex=r'^$',
        view=views.HomePageView.as_view(),
        name='home'
    ),
    url(
        regex=r'^event/$',
        view=views.EventListView.as_view(),
        name='event_list'
    ),
    url(
        regex=r'^event/team/$',
        view=views.TeamListView.as_view(),
        name='team_list'
    ),
    url(
        regex=r'^event/team/(?P<team_id>[\w.@+-]+)/(?P<action>(join|leave))/$',
        view=views.join_team,
        name='team_join'
    ),
    url(
        regex=r'^event/(?P<pk>[\w.@+-]+)/$',
        view=views.EventDetail.as_view(),
        name='event_detail'
    ),
    url(
        regex=r'^event/(?P<pk>[\w.@+-]+)/vote/$',
        view=views.ValueView.as_view(),
        name='vote_detail'
    ),
    url(
        regex=r'^event/(?P<pk>[\w.@+-]+)/result/$',
        view=views.ResultView.as_view(),
        name='result'
    ),
    url(
        regex=r'^profile/(?P<pk>[\w.@+-]+)/$',
        view=views.ProfileDetail.as_view(),
        name='profile'
    ),

]
