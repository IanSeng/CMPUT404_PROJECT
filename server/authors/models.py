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


class Follow(models.Model):
    '''
    TODO make a controller class that queries for 
    - list of authors following you
    - list of authors you are following
    - list of friends (they follow you AND you follow them)
    '''
    follower = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="followed")

    def get_follower(self):
        return self.follower

    def get_followed(self):
        return self.followed

    class Meta:
        constraints = [
            # Ensuring each follow is unique
            # From Django Docs
            # https://docs.djangoproject.com/en/dev/ref/models/constraints/#uniqueconstraint
            models.UniqueConstraint(
                fields=["follower", "followed"], name="unique_follow"),

            # Enforcing 2 unique DB columns
            # From StackOverflow https://stackoverflow.com/a/64376614
            # From Ali Shekari https://stackoverflow.com/users/7978891/ali-shekari
            models.CheckConstraint(check=~models.Q(follower=models.F(
                'followed')), name='follower_not_equal_to_followed')
        ]

    def __str__(self):
        return f"{self.follower.user.username} follows {self.followed.user.username}"
