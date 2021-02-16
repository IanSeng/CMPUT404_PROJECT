from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from authors.models import Author


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # TODO: use access token to figure out user in the future?
    def perform_create(self, serializer):
        serializer.save(author=Author.objects.get(user=self.request.user.id))
