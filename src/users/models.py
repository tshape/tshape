from __future__ import unicode_literals

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
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        profile = Profile(
            user=user,
        )
        profile.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        abstract = False
        db_table = 'users'
        app_label = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    email = models.EmailField(
        _('email address'), null=False, unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        }
    )
    username = models.CharField(
        _('username'), max_length=30, unique=True, blank=True, null=True
    )
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    first_name = models.CharField(
        _('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(
        _('last name'), max_length=50, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
