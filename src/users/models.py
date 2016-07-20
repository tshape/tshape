from __future__ import unicode_literals

from django.core import validators
from django.core.mail import send_mail
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from profiles.models import Profile


class UserManager(BaseUserManager):

    def create(self, email, password=None, *args, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        profile = Profile(
            user=user,
        )
        profile.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    class Meta(object):
        abstract = False
        db_table = 'users'
        app_label = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    email = models.EmailField(
        _('Email Address'), null=False, unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        }
    )
    username = models.CharField(
        _('Username'), max_length=30, unique=True, blank=True, null=True,
        help_text=_('30 characters or fewer. Letters, digits and _ only.'),
        validators=[
            validators.RegexValidator(
                r'^\w+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers and _ character.'),
                'invalid'
            ),
        ],
        error_messages={
            'unique': _("The username is already taken."),
        }
    )
    is_staff = models.BooleanField(
        _('Staff Status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email
