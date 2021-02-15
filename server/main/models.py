from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.core.validators import RegexValidator

import uuid
import re

class UserManager(BaseUserManager):
    def create_author(self, username, password):
        author = self.model(username=re.sub(r'\W+', '', username))
        author.set_password(password)
        author.save(using=self._db)

        return author

    def create_superuser(self, username, password):
        user = self.create_author(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Author(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=25, unique=True)
    display_name = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
