from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


from .forms import SignUpForm, CreateTeamForm
from .tokens import account_activation_token

from .models import User
from voting.votingmachine.models import Event, Team, Value


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def all_events(self):
        return Event.objects.all()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return reverse('admin:index')

        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['first_name', 'last_name', 'username', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username, first_name=self.request.user.first_name, last_name=self.request.user.last_name)


class UserUpdateEmailView(LoginRequiredMixin, UpdateView):
        fields = ['username', ]

        # we already imported User in the view code above, remember?
        model = User

        # send the user back to their own page after a successful update
        def get_success_url(self):
            return reverse('users:detail',
                           kwargs={'username': self.request.user.username})

        def get_object(self):
            # Only get the User record for the user making the request
            return User.objects.get(username=self.request.user.username, )


class UserUpdatePasswordView(LoginRequiredMixin, UpdateView):
    fields = ['password', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(password=self.request.user.password, )


class HomePageView(TemplateView):
    template_name = 'votingmachine/home.html'


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def create_team(request):
    if request.method == 'POST':
        form1 = CreateTeamForm(request.POST)
        if form1.is_valid():
            new_team = form1.save()
            return redirect('home')
    else:
        form1 = CreateTeamForm()
        form1.initial = {'leader': request.user}
    return render(request, 'users/user_create_team.html', {'form1': form1})


def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'users/account_activation_invalid.html')


def logout_view(request):
    logout(request)
    return redirect('home')


