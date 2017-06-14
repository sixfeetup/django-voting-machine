from django.db import models
from django.db.models import Avg, Count, Sum
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth import get_user_model as user_model
User = user_model()


class Event(models.Model):
    WEIGHT_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    )
    STATE_CHOICES = (
        ('S', 'Setup'),
        ('A', 'Active'),
        ('P', 'Paused'),
        ('F', 'Finished')
    )
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.CharField(max_length=2048, default='')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, default='')
    state = models.CharField(max_length=3, choices=STATE_CHOICES, default='S')
    weighted = models.CharField(max_length=5, choices=WEIGHT_CHOICES, default=0)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, default=timezone.now)
    end_date = models.DateField(null=True)

    def results(self):
        teams = Team.objects.filter(event=self).order_by('?')
        sorted_teams = sorted(teams, key=lambda team: team.get_score(), reverse=True)
        return sorted_teams

    def __str__(self):
        return " %s :  %s" % (self.title, self.description)


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

    class Meta:
        unique_together = [('user', 'event', 'category', 'team')]

    def user_already_voted(self, user):
        if not Value.objects.filter(event=self.id, user=user.id, category=self.id):
            return True
        else:
            return False

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.date = timezone.now()
        super(Value, self).save(self, force_insert, force_update, using)

    def __str__(self):
        return '%s votes %s' % (self.user, self.get_votes_display())


class Team(models.Model):
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.CharField(max_length=2048, blank=True, default='')
    members = models.ManyToManyField(User)
    leader = models.ForeignKey(User, on_delete=models.PROTECT, related_name="leads")
    event = models.ForeignKey(Event, on_delete=models.PROTECT)

    class Meta:
        ordering = ["title"]

    # @classmethod
    # def create(csl, title, description, members, leader, event):
    #     team = csl(title=title, description=description, members=members, leader=leader, event=event)
    #     return team
    #
    # def create_team(self, title, description, members, leader, event):
    #     team = self.create(title=title, description=description, members=members, leader=leader, event=event)
    #     return team
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

    def total_final_result(self):
        return (self.get_total_score() / int(Event.weighted)) * 100

    @property
    def all_members(self, **kwargs):
        return self.members.order_by('id').all()

    def __str__(self):
        return " %s :  %s" % (self.title, self.description)
