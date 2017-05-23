from django.conf.urls import url

from . import views
from .views import HomePageView, TeamListView, EventListView, EventDetail, ProfileDetail, ResultDetail

#app_name = 'votingmachine'
urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^team/$', TeamListView.as_view(), name='team_list'),
    url(r'^event/$', EventListView.as_view(), name='event_list'),
    url(r'^event/(?P<pk>\d+)/$', EventDetail.as_view(), name='event_detail'),
    url(r'^profile/(?P<pk>[\w-]+)/$', ProfileDetail.as_view(), name="profile"),
    #url(r'^result$', ResultDetail.as_view(), name='result'),
    url(r'^voting/$', views.voting, name='voting'),

    url(r'^search/$', views.search, name='search'),
]
