from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Author
from posts.models import Post


class Inbox(models.Model):
    # TODO add like and follow
    type = "inbox"
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, blank=True)

# TODO create object when Author is created
# @receiver(post_save, sender=Author)
# def my_handler(sender, **kwargs):
#     if sender.pk is None:  # create
#         sender.model = Inbox.objects.create(author=sender)