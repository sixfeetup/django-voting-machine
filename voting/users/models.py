
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    username = models.EmailField(_('Email Address'), blank=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=100, blank=True, default='', help_text='Optional.')
    last_name = models.CharField(max_length=256, blank=True, default='', help_text='Optional.')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


