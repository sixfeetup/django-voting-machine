from django.forms import ModelForm
from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'owner', 'state', 'weighted',  'start_date', 'end_date']
