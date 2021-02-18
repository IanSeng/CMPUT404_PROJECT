from django.db import models

# Node that we share information with
class Node(models.Model):
    type = "node"

    remote_server_url = models.URLField(max_length=200, primary_key=True, unique=True)
    remote_server_username = models.CharField(max_length=200, default='', blank=True)
    remote_server_password = models.CharField(max_length=200, default='', blank=True)
    adminApproval = models.BooleanField(default=False)

    konnection_username = models.CharField(max_length=200, default='', blank=True)
    konnection_password = models.CharField(max_length=200, default='', blank=True)
