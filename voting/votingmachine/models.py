from django.db import models
from django.db.models import Avg, Count, Sum
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model as user_model
from django.utils.datetime_safe import datetime
from pytz import UTC

User = user_model()


class EventManager(models.Manager):
    def active(self):
        return self.filter(state='A')


class Event(models.Model):
    WEIGHT_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    )
    STATE_CHOICES = (
        ('A', 'Active'),
        ('F', 'Finished')
    )
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.CharField(max_length=2048, default='')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, default='')
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='A')
    weighted = models.CharField(max_length=5, choices=WEIGHT_CHOICES, default=0)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('start_date',)

    objects = EventManager()

    def winner(self):
        teams = self.team_set.all()
        ranked_teams = []
        sorted_teams = sorted(teams, key=lambda team: team.total_final_result(), reverse=True)
        for team in sorted_teams:
            scores = self.result_position(sorted_teams)
            rank = scores.index(
                team.total_final_result()
            ) + 1
            ranked_teams.append({
                "team": team,
                "opacity": self.result_opacity(len(scores), rank),
                "rank": rank
            })
        return ranked_teams

    def status(self):
        now = datetime.now(tz=UTC)
        if self.start_date < now < self.end_date:
            return 'open'
        elif self.end_date < now:
            return 'closed'
        elif self.start_date > now:
            return 'upcoming'

    def __str__(self):
        return " %s :  %s" % (self.title, self.description)

    def is_user_ballot_complete(self, user):
        """check that the user has Values for every team and category they are allowed to vote for, within this event
        
        """
        # teams = self.team_set.all()
        # value = self.value_set.all()
        #
        # for user in self.user

    def result_opacity(self, count, rank):
        # we don't want to go all the way to 0 opacity,
        # so we get increments based on .7 instead of 1
        increment = .7 / count
        return 1-(rank * increment)-.2

    def result_position(self, sorted_teams):
        totals = []
        for team in sorted_teams:
            totals.append(team.total_final_result())
        scores = list(set(totals))
        return sorted(scores, reverse=True)


class Value(models.Model):
    VOTES_CHOICES = (
        (+1, '1'),
        (+2, '2'),
        (+3, '3')
    )
    CATEGORY_CHOICES = (
        ('U', 'Useful'),
        ('A', 'Awesome'),
        ('C', 'Completion')
    )
    votes = models.IntegerField(choices=VOTES_CHOICES, default=+1)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, default='', on_delete=models.PROTECT)
    team = models.ForeignKey('Team', null=True, on_delete=models.PROTECT)
    # complete = models.BooleanField(default=True)

    class Meta:
        unique_together = [('user', 'event', 'category', 'team')]

    def user_already_voted(self, user):
        if not Value.objects.filter(event=self.id, user=user.id, category=self.id):
            return True
        else:
            return False

    def __str__(self):
        return '%s votes %s for %s %s' % (self.user, self.get_votes_display(), self.category, self.team)


class Team(models.Model):
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.CharField(max_length=2048, blank=True, default='')
    members = models.ManyToManyField(User)
    leader = models.ForeignKey(User, on_delete=models.PROTECT, related_name="leads")
    event = models.ForeignKey(Event, on_delete=models.PROTECT)

    class Meta:
        ordering = ["title"]

    @property
    def all_members(self):
        return set([self.leader,] + list(self.members.order_by('id').all()))

    def count_members(self):
        return len(self.all_members)

    def count_event_team_all_members(self):
        team_member_count = 0
        for team in Team.objects.filter(event=self.event):
            team_member_count += team.count_members()
        return team_member_count

    def get_votes(self, category):
        return Value.objects.filter(event=self.event, category=category, team=self)

    def get_category_score(self, category):
        cat_score = sum(self.get_votes(category).values_list('votes', flat=True))
        return cat_score

    def get_total_score(self):
        tot_score = 0
        for cat in Value.CATEGORY_CHOICES:
            cat_score = self.get_category_score(cat[0])
            tot_score += cat_score
        return tot_score

    def divscore_members(self):
        if self.count_event_team_all_members() == self.count_members():
            return 0
        else:
            divi = self.get_total_score() / (self.count_event_team_all_members()-self.count_members())
            return divi / int(self.event.weighted)

    def total_final_result(self):
        return self.divscore_members() / int(self.event.weighted) *100

    def __str__(self):
        return " %s :  %s" % (self.title, self.description)
