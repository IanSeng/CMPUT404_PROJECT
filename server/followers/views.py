from django.shortcuts import render
from rest_framework import generics, permissions

from main import models
from followers.serializers import FollowersSerializer

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.contrib.auth import get_user_model
# Create your views here.
class FollowersView(generics.ListAPIView):
    serializer_class = FollowersSerializer
    permission_classes = [permissions.IsAuthenticated]
    # queryset = models.Followers.objects.all()
    
    def get_queryset(self):
        request_author_id = self.kwargs['id']
       
        try:
            return models.Followers.objects.filter(author=request_author_id)
        except:
            raise ValidationError({"error": ["User not found"]})
        # print(models.Followers.objects.all())