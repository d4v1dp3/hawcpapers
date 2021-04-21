from django.contrib.auth.base_user import BaseUserManager

import logging

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user, name, surname, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not user or not name or not surname or not email:
            raise ValueError('The given usernames data must be set')

        mail = self.normalize_email(email)
        newuser = self.model(user=user, name=name, surname=surname, **extra_fields)
        newuser.set_password(password)
        newuser.email = mail
        newuser.save(using=self._db)
        return newuser

    def create_user(self, user, name, surname, emails, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(user, name, surname, emails, password, **extra_fields)

    def create_superuser(self, user, name, surname, emails, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user, name, surname, emails, password, **extra_fields)
