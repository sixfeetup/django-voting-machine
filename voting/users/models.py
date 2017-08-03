
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django_fsm import FSMField, transition
# from django_fsm_log.decoratora import fsm_log_by


@python_2_unicode_compatible
class User(AbstractUser):

    STATUS_NEW = 'N'
    STATUS_APPROVED = 'A'
    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_APPROVED, 'Approved'),
    )
    # First Name and Last Name do not cover name patterns
    # around the globe.
    username = models.EmailField(_('Email Address'), blank=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=100, blank=True, default='', help_text='Optional.')
    last_name = models.CharField(max_length=256, blank=True, default='', help_text='Optional.')
    state = FSMField(
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    class Meta:
        ordering = ( 'first_name', 'last_name',)

    # @fsm_log_by
    @transition(
        field=state,
        source=STATUS_NEW,
        target=STATUS_APPROVED,
    )
    def approve(self, by=None):
        '''send to user for approval'''
        # TODO send an e-mail notification
        pass
        from django.core.mail import send_mail
        send_mail("VotingMachine",
                  "Your email has been approved, we are happy to have you on board!",
                  "admin@sixfeetup.com", [self.username],
                  fail_silently=False,
                  )

    @transition(
        field=state,
        source=STATUS_APPROVED,
        target=STATUS_NEW,
    )
    def unapprove(self, by=None):
        '''send to user back to new'''
        pass

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


