from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User

import uuid
import re
from main import utils

class UserManager(BaseUserManager):
    def create_author(self, username, password, **extra_fields):
        author = self.model(username=re.sub(r'\W+', '', username), **extra_fields)
        author.set_password(password)
        author.save(using=self._db)

        return author

    def create_superuser(self, username, password):
        user=self.create_author(username, password)
        user.is_superuser=True
        user.is_staff=True
        user.type=utils.UserType.superuser
        user.save(using=self._db)

        return user


class Author(AbstractBaseUser, PermissionsMixin):
    # Required objects
    type=models.CharField(max_length=25, default=utils.UserType.author.value)
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host=models.CharField(max_length=253, default=utils.HOST)
    displayName=models.CharField(max_length=255)
    # TODO: Append host once we have host IP
    url= models.CharField(max_length=255, default='')
    github=models.CharField(max_length=255, default='')

    username = models.CharField(max_length=25, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
