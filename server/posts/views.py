from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from django.contrib.auth import get_user_model
from main import models as mainModels


class CreatePostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # TODO: use access token to figure out current user
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=mainModels.Author.objects.get(id=self.request.user.id))
