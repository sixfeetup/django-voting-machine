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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    state = models.CharField(max_length=3, choices=STATE_CHOICES, default='S')
    weighted = models.CharField(max_length=5, choices=WEIGHT_CHOICES, default=0)
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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='M')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='events')

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return ' %s Status= %s' % (self.user.username, self.status)


class Vote(models.Model):
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
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event, default='')

    class Meta:
        unique_together = [('user', 'event', 'category')]

    def user_already_voted(self, user):
        if not Vote.objects.filter(event=self.id, user=user.id, category=self.id):
            return True
        else:
            return False

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.date = timezone.now()
        super(Vote, self).save(self, force_insert, force_update, using)

    def __str__(self):
        return '%s votes %s' % (self.user, self.get_votes_display())


class Team(models.Model):
    title = models.CharField(max_length=256, unique=True, default='')
    description = models.CharField(max_length=2048, blank=True, default='')
    leader = models.ForeignKey(Profile, default='Member', related_name='leaders')
    members = models.ManyToManyField(Profile, verbose_name="list of members")
    #votes = models.ForeignKey(Vote, default=0, related_name='vote')

    # count = models.PositiveIntegerField(default=0)
    # average = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.0))

    class Meta:
        ordering = ["title"]

    def total_final(self):
        return (self.average / Event.weighted) * 100

    def avg_for_team(self):
        for e in Event.objects.all():
            for t in Team.objects.all():
                vmt = sum(Team.votes.objects.all())/(sum(t.members()) * Event.weighted)
                return vmt

    @property
    def all_members(self, **kwargs):
        return self.members.order_by('id').all()

    def __str__(self):
        return " %s :  %s" % (self.title, self.description)






