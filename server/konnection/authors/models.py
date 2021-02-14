from django.db import models
import uuid
from django.contrib.auth.models import User


class Author(models.Model):
    # TODO use django's built User class to authenticate username/password
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Using Django unique identifiers
    # From Django Docs
    # From https://docs.djangoproject.com/en/3.1/ref/models/fields/#uuidfield
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=200)
    github_url = models.URLField(blank=True, null=True)
    admin_approved = models.BooleanField(default=False)

    # TODO return format http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e
    # Need hostname
    def get_url(self):
        pass

    def get_id(self):
        return self.id

    def get_display_name(self):
        return self.display_name

    def set_display_name(self, new_name):
        self.display_name = new_name

    def get_github_url(self):
        return self.github_url

    def set_github_url(self, new_url):
        self.github_url = new_url

    def __str__(self):
        return self.user.username
