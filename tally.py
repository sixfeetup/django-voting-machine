from decimal import Decimal
from django.db import models
from django.db.models import Avg, Count, Sum
from voteapp.models import Event, Team, Profile, Voting

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

tallies = {}
for e in [ Event.objects.last()]:
    for p in e.profile.all():
        for t in Team.objects.exclude(id__in=[x.id for x in p.team_set.all()]):
            if t not in tallies:
                tallies[t] = {'U': (0, 0), 'A': (0, 0), 'C': (0, 0)}
            profile_votes = p.user.voting_set.filter(team=t)
            for c in "UAC":
                c_vote = profile_votes.filter(criteria__exact=c).first()
                tallies[t][c][0] += 1
                tallies[t][c][1] += int(c_vote.votes)

for t, criteria_dict in tallies.items():
    for c in criteria_dict.keys():
        criteria_votes = criteria_dict[c]
        mean = criteria_votes[1] / 1.0 * criteria_votes[0]
