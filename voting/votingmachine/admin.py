from django.contrib import admin
from django import forms
from searchableselect.widgets import SearchableSelect

from .models import Event, Team, Value
from django.contrib.auth import get_user_model as user_model
User = user_model()


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date']
    list_filter = ['title', 'start_date', 'end_date']
admin.site.register(Event, EventAdmin)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ()
        widgets = {
            'members': SearchableSelect(model='users.User',
                                        search_field='username',
                                        many='True', limit=10
                                        )
        }


class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader', 'all_members', 'description']
    list_filter = ['title', 'description']
    form = TeamForm
admin.site.register(Team, TeamAdmin)


class ValueAdmin(admin.ModelAdmin):
    list_display = ['event', 'team', 'user', 'category', 'votes']
    list_filter = ['event', 'team', 'user', 'category', 'votes']
    ordering = ['event']
admin.site.register(Value, ValueAdmin)
