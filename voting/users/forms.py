from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from voting.votingmachine.models import Team, Event
#from voting.users.models import User

User = get_user_model()


class SignUpForm(UserCreationForm):
    username = forms.EmailField(max_length=254, help_text='Required. Your email address will be your username.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )


class CreateTeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('title', 'description', 'members', 'leader', 'event')
    event = forms.ModelChoiceField(queryset=Event.objects.all().filter(state="A"))
