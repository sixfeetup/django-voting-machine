from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json


from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Event, Team, Value
from django.contrib.auth import get_user_model as user_model
User = user_model()


class HomePageView(TemplateView):
    template_name = 'votingmachine/home.html'

    # def get_context_data(self, **kwargs):
    #     context = super(HomePageView, self).get_context_data(**kwargs)
    #     context['events'] = Event.objects.all()
    #     return context


class TeamListView(LoginRequiredMixin, ListView):
    redirect_field_name = 'redirect_to'
    model = Team


class EventListView(LoginRequiredMixin, ListView):
    redirect_field_name = 'redirect_to'
    model = Event


class EventDetail(LoginRequiredMixin, DetailView):
    redirect_field_name = 'redirect_to'
    model = Event
    template_name = 'votingmachine/event_detail.html'


class ProfileDetail(LoginRequiredMixin, DetailView):
    redirect_field_name = 'redirect_to'
    model = User
    template_name = 'votingmachine/profile.html'
    #use username instead of pk
    # slug_field = "username"
    # slug_field = 'user'
    # slug_url_kwarg = 'user'
    # override the context user object from user to user_profile, use {{ user_profile }} instead of {{ Profile }} in template
    #context_object_name = "user_profile"


class ValueView(LoginRequiredMixin, TemplateView):
    redirect_field_name = 'redirect_to'
    model = Value
    template_name = 'votingmachine/voting_detail.html'
    select_related = 'user'
    context_vote_name = 'votes'
    template_name_suffix = '_voted_by'

    def get_context_votes_name(self):
        return self.context_vote_name

    def get_votes(self, obj):
        queryset = self.get_votes(obj)
        if self.select_related:
            queryset = queryset.select_related(self.select_related)
        return queryset


class ResultView(LoginRequiredMixin, TemplateView):
    redirect_field_name = 'redirect_to'
    model = Value
    template_name = 'votingmachine/result.html'

    # def top_voted(self):
    #     return self(score=Sum('votes')).order_by('score')


def search(request):
    events = Event.objects.filter(title__contains=request.GET['title'])
    return render(request, 'votingmachine/home.html', {"events": events})


def add_user_to_team(user, team):
    team = Team.objects.get(id=team.id)
    team.members.add(user)
    team.save()
    return


def remove_user_from_team(user, team):
    group = Team.objects.get(id=team.id)
    group.members.remove(user)
    group.save()
    return


@login_required
def join_team(request, team_id, action):
    try:
        user = request.user
        team = Team.objects.get(id=team_id)
        if action == 'join':
            add_user_to_team(user, team)
        elif action == 'leave':
            remove_user_from_team(user, team)
        else:
            raise Exception( "unexpected action:" + action)
        to_json = {
            'status': "OK",
        }
    except Exception as e:
        to_json = {'status': 'FAIL',  'message': 'Could not join team.', 'reason': str(e)}

    return HttpResponse(json.dumps(to_json), content_type='application/json')






# def add_user_to_team(user, team):
#     group = Group.objects.get(id=team.id)
#     group.user_set.add(user)
#     group.save()
#     return

# def join_team(request, team_id):
#     user = request.user
#     team = Team.objects.get(id=team_id)
#     if not team:
#         return not_found()
#     add_user_to_team(user, team)
#     return HttpResponseRedirect('home')
#
# def remove_user_from_team(user, team):
#     group = Team.objects.get(id=team.id)
#     group.members.remove(user)
#     group.save()
#     return
