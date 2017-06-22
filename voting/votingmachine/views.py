from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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


class ValueView(LoginRequiredMixin, TemplateView):
    redirect_field_name = 'redirect_to'
    model = Value
    template_name = 'votingmachine/vote_detail.html'
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

@login_required
def vote_page(request, pk):
    event = Event.objects.get(id=pk)
    cats = Value.CATEGORY_CHOICES
    return render(request, 'votingmachine/vote_detail.html', {'event':event, 'cats':cats} )


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
            raise Exception("unexpected action:" + action)
        to_json = {
            'status': "OK",
        }
    except Exception as e:
        to_json = {'status': 'FAIL',  'message': 'Could not join team.', 'reason': str(e)}

    return HttpResponse(json.dumps(to_json), content_type='application/json')


def add_value_to_vote(votes, value):
    result = Value.objects.get(id=value.id)
    result.members.add(votes)
    result.save()
    return




from django.core.exceptions import PermissionDenied


def get(self, request, *args, **kwargs):
    team_id = self.kwargs.get('team_id')
    team = Team.objects.get(pk=team_id)
    if team_id == team:
        raise PermissionDenied
    else:
        return super(collect_vote, self).get(request, *args, **kwargs)

@require_POST
@login_required
def collect_vote(request, pk):
    u_id = request.user.id
    t_id = request.POST['team_id']
    cat = request.POST['category']
    value_id = int(request.POST['value'])
    # ensure the user is not voting for their own teams:
    team = Team.objects.get(id=t_id)
    if request.user in team.all_members:
        return HttpResponse("You cannot vote for your own team.", content_type="text/plain")

    (vote, is_new) = Value.objects.get_or_create(
        user=User.objects.get(pk=u_id),
        team=Team.objects.get(pk=t_id),
        event=Event.objects.get(pk=pk),
        category=cat,
        defaults={'votes':value_id})
    if not is_new:
        vote.votes = value_id
        vote.save()

    return HttpResponse("Success", content_type="text/plain")


class ResultView(LoginRequiredMixin, DetailView):
    model = Event
    # These next two lines tell the view to index lookups by username
    slug_field = 'id'
    slug_url_kwarg = 'pk'
    template_name = 'votingmachine/result.html'

