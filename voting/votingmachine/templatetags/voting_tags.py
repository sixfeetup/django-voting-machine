from django import template

from voting.votingmachine.models import Value

register = template.Library()


@register.simple_tag
def check_selected(user_id, event_id, category, team_id, btn_value):
    try:
        buttonval = Value.objects.get(
            user=user_id,
            team=team_id,
            event=event_id,
            category=category)
        if btn_value == buttonval.votes:
            return 'btn-primary'
        else:
            return 'btn-secondary'
    except Value.DoesNotExist:
        return 'btn-secondary'
