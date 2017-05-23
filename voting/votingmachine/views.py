from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Event, Team, Profile, Voting, Result


class HomePageView(TemplateView):
    template_name = 'voting/templates/pages/home.html'

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
    template_name = 'voteapp/event_detail.html'


class ProfileDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Profile
    template_name = 'voteapp/profile.html'
    #use username instead of pk
    # slug_field = "username"
    # override the context user object from user to user_profile, use {{ user_profile }} instead of {{ Profile }} in template
    #context_object_name = "user_profile"



#class Voting
@login_required(login_url="/")
def voting(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    try:
        selected_category = category.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Category.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'voteapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('voteapp:results', args=(question.id,)))


class ResultDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Result
    template_name = 'voteapp/result.html'


def search(request):
    events = Event.objects.filter(title__contains=request.GET['title'])
    return render(request, 'voteapp/home.html', {"events": events})

