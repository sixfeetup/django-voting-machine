from django.conf.urls import url

from . import views
from .views import HomePageView, TeamListView, EventListView, EventDetail, ProfileDetail, ResultDetail

app_name = 'votingmachine'
urlpatterns = [
    url(
        regex=r'^$',
        view=views.HomePageView.as_view(),
        name='home'
    ),
    url(
        regex=r'^team/$',
        view=views.TeamListView.as_view(),
        name='team_list'
    ),
    url(
        regex=r'^event/$',
        view=views.EventListView.as_view(),
        name='event_list'
    ),
    url(
        regex=r'^event/(?P<pk>\d+)/$',
        view=views.EventDetail.as_view(),
        name='event_detail'
    ),
    url(
        regex=r'^profile/(?P<pk>[\w-]+)/$',
        view=views.ProfileDetail.as_view(),
        name='profile'
    ),
    url(
        regex=r'^voting/$',
        view=views.voting,
        name='voting'
    ),
    #url(r'^result$', ResultDetail.as_view(), name='result'),
]
