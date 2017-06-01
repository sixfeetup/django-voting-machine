from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from searchableselect.widgets import SearchableSelect

from .models import Event, Profile, Team, Vote


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date']
    list_filter = ['title', 'start_date', 'end_date']
admin.site.register(Event, EventAdmin)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ()
        widgets = {
            'members': SearchableSelect(model='votingmachine.Profile',
                                        search_field='user__username',
                                        many='True', limit=100
                                        )
        }


class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader', 'all_members', 'description']
    list_filter = ['title', 'description']
    form = TeamForm
admin.site.register(Team, TeamAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']
    list_filter = ['user', 'status']
    fieldsets = [
        (None, {'fields': ['user']}),
        (None, {'fields': ['status']}),
        ('Event', {'fields': ['event']}),
    ]
admin.site.register(Profile, ProfileAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'category', 'votes']
    list_filter = ['event', 'user', 'category', 'votes']
    ordering = ['event']
admin.site.register(Vote, VoteAdmin)
