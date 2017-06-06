from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.db.models import Sum


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
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Team


class EventListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Event


class EventDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Event
    template_name = 'votingmachine/event_detail.html'


class ProfileDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
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
    login_url = '/login/'
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
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Value
    template_name = 'votingmachine/result.html'

    # def top_voted(self):
    #     return self(score=Sum('votes')).order_by('score')


def search(request):
    events = Event.objects.filter(title__contains=request.GET['title'])
    return render(request, 'votingmachine/home.html', {"events": events})


class ProofView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Team
    template_name = 'votingmachine/proof.html'
