import datetime

from django.db import models

from datetime import date, datetime

from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .usermanager import UserManager

import logging

logger = logging.getLogger(__name__)


# Create your models here.

class Major(models.Model):
    name = models.CharField(max_length=30)


class Email(models.Model):
    email = models.EmailField(null=False, blank=False)


class Phone(models.Model):
    phone = models.CharField(max_length=40)


class Social(models.Model):
    account = models.CharField(max_length=40)
    service = models.CharField(max_length=20)


class Paper(models.Model):
    number = models.IntegerField(null=False)
    title = models.CharField(max_length=100)
    journal = models.CharField(max_length=30)
    signup_due = models.DateField(default=date.today)

    user = ''

    def set_user(self, user):
        self.user = user

    @property
    def signed_by_user(self):
        sign = self.publication_set.get(paper_id=self.id, author__user=self.user)
        if sign:
            return sign.status
        return 'Not signed'


class Institution(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    webpage = models.CharField(max_length=50)
    publications = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)


class Author(AbstractBaseUser, PermissionsMixin):
    user = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=False, blank=False)
    # Extra Fields
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    address = models.CharField(max_length=50, blank=True)
    emails = models.ManyToManyField(Email)
    phones = models.ManyToManyField(Phone)
    socials = models.ManyToManyField(Social)
    major = models.ForeignKey(Major, on_delete=models.DO_NOTHING, null=True)
    q_author = models.BooleanField(default=False)
    sign_safe = models.BooleanField(default=False)
    valid = models.DateField(null=True)
    name_full = models.CharField(max_length=30, blank=True)
    name_swapped = models.CharField(max_length=30, blank=True)
    initialed_full = models.CharField(max_length=30, blank=True)
    initialed_swapped = models.CharField(max_length=30, blank=True)
    contact = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    web_page = models.CharField(max_length=40, blank=True)
    activities = models.TextField(blank=True)
    country = models.CharField(max_length=20, blank=True)
    paper = models.ManyToManyField(Paper, through='Publication')

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = ['name', 'surname', 'email']
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.user

    # def has_perm(self, perm, obj=None):
    #    "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
    #    return True

    #def has_module_perms(self, app_label):
    #    "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
    #    return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def full_name(self):
        """Returns the person's full name."""
        return '%s %s' % (self.name, self.surname)

    @property
    def get_short_name(self):
        """Returns the short name for the user."""
        return self.name

    def add_mail(self, email):
        try:
            mail = Email(email=email)
            mail.save()
            self.emails.add(mail)
        except Exception as e:
            raise ValueError('Error adding email: %s to user: %s -> %s' % (email, self.user, e))

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Publication(models.Model):
    class Status(models.TextChoices):
        ACCEPT = 'A', _('Signed')
        REJECT = 'R', _('Reject')

    paper = models.ForeignKey(Paper, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=Status.choices)
    sign_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        unique_together = ('paper', 'author')
