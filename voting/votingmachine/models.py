from django.db import models
from django.contrib.auth.models import User
#, Group
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    state = models.CharField(max_length=3, choices=STATE_CHOICES, default='S')
    weighted = models.CharField(max_length=5, choices=WEIGHT_CHOICES, default='0')
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, default=timezone.now)
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    STATUS_CHOICES = (
        ('L', 'Leader'),
        ('M', 'Member')
    )
    STATUSES = [t[0] for t in STATUS_CHOICES]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='M')
    event = models.ForeignKey(Event, related_name='events')

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return ' %s Status= %s' % (self.user.username, self.status)


class Team(models.Model):
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.CharField(max_length=2048, blank=True, default='')
    leader = models.ForeignKey(Profile, default='Member', related_name='leaders')
    members = models.ManyToManyField(Profile, verbose_name="list of members")

    class Meta:
        ordering = ["title"]

    @property
    def all_members(self):
        return self.members.order_by('id').all()

    def __str__(self):
        return " %s :  %s" % (self.title, self.description)


class Voting(models.Model):
    VOTES_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3')
    )
    CATEGORY_CHOICES = (
        ('U', 'Useful'),
        ('A', 'Awesome'),
        ('C', 'Completion')
    )
    votes = models.SmallIntegerField(choices=VOTES_CHOICES, default=1)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='')
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    event = models.ForeignKey(Event, default='')

    class Meta:
        unique_together = [('user', 'event', 'category')]

    def __str__(self):
        return self.get_votes_display()


class Result(models.Model):
    VOTES_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3')
    )
    result = models.SmallIntegerField(choices=VOTES_CHOICES, default=1)
