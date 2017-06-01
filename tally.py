from decimal import Decimal
from django.db import models
from django.db.models import Avg, Count, Sum
from .models import Event, Team, Profile, Voting

# for e in [Event.objects.last()]:
#     for t in e.Team_set.all():
#         for vt in e.team_set.exclude(team=t):
#             for c in [ 'U', 'A', 'C']:
#                 print (e, t, vt, c)
#
#         vt_te_cri_aver = Avg(Voting.objects.exclude(team=t).filter(criteria=c).values(['voting']))
#         vote_avgs[t][c][vt] = vt_te_cri_aver
# t_c_avg = Avg(Voting.c.avg[t][c].items)

# if not tallies.has_key(t): = if t not in tallies
#
# tallies = {}
# for e in [ Event.objects.last()]:
#     for p in e.profile.all():
#         for t in Team.objects.exclude(id__in=[x.id for x in p.team_set.all()]):
#             if t not in tallies:
#                 tallies[t] = {'U': (0, 0), 'A': (0, 0), 'C': (0, 0)}
#             profile_votes = p.user.voting_set.filter(team=t)
#             for c in "UAC":
#                 c_vote = profile_votes.filter(criteria__exact=c).first()
#                 tallies[t][c][0] += 1
#                 tallies[t][c][1] += int(c_vote.votes)
#
# for t, criteria_dict in tallies.items():
#     for c in criteria_dict.keys():
#         criteria_votes = criteria_dict[c]
#         mean = criteria_votes[1] / 1.0 * criteria_votes[0]


tallies = dict()
for e in Event.objects.all():
    for p in Profile.objects.all():
        for t in Team.objects.exclude(id=[x.id for x in p.team_set.all()]):
            if t not in tallies:
                tallies[t] = {'U': (0, 0), 'A': (0, 0), 'C': (0, 0)}
            profile_votes = p.user.voting_set.filter(team=t)
            for c in [ 'U', 'A', 'C']:
                c_votes = profile_votes.filter(criteria__exact=c).first()
                tallies[t][c][0] += 1
                tallies[t][c][1] += int(c_votes.votes)

for t, criteria_dict in tallies.items():
    for c in criteria_dict.keys():
        criteria_votes = criteria_dict[c]
        mean = criteria_votes[1]/1.0 * criteria_votes[0]
    vt_te_cri_avg = Avg(Vote.objects.exclude(team=t).filter(criteria_votes=c).values({'vote'}))
    vote_avgs[t][c][t] = vt_te_cri_avg
t_c_avg = Avg(Vote.c.avg[t][c].items)


class Result(models.Model):
    VOTES_CHOICES = (
        (+1, '1'),
        (+2, '2'),
        (+3, '3')
    )
    count = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    result = models.SmallIntegerField(choices=VOTES_CHOICES, default=+1)
    average = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.0))

    @property
    def percentage(self):
        return (self.average / 3) * 100

    def to_dict(self):
        return {
            'count': self.count,
            'total': self.total,
            'average': self.average,
            'percentage': self.percentage,
        }

    def calculate(self):
        """
        Recalculate the totals, and save.
        """
        aggregates = self.result.a(total=Sum('score'), average=Avg('score'), count=Count('score'))
        self.count = aggregates.get('count') or 0
        self.total = aggregates.get('total') or 0
        self.average = aggregates.get('average') or 0.0
        self.save()


    # def calculate_aver_votes_for_team(self):
    #     for e in Event.objects.all():
    #         for t in Team.objects.all():
    #             for v in Vote.objects.all():
    #                 if v not in Vote:
    #                     return 0
    #                 else:
    #                     votes_aver_mem_team = Sum(Vote.objects.exclude(Team != t, )) /count
    #                     return votes_aver_mem_team
    #     return self.calculate_aver_votes_for_team()

    # def av_team(self):
    #     p = Vote.objects.get(*args, **kwargs)
    #     vote_team_average = p.
