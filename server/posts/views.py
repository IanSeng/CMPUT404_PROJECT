from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from main import models as mainModels
from .models import Post
from .serializers import PostSerializer


# service/author/{AUTHOR_ID}/posts/{POST_ID}
class UpdatePostView(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # GET: get_queryset is called after a GET command
    def get_queryset(self):
        request_author_id = self.kwargs['author_id']
        request_post_id = self.kwargs['post_id']

        # TODO: allow friends to view the post too
        if (self.request.user.id == request_author_id):
            queryset = Post.objects.filter(id=request_post_id)
        else:
            queryset = Post.objects.filter(
                id=request_post_id,
                visibility=Post.PUBLIC
            )
        return queryset # returns [] if post visibility is Friend or was deleted
    
    # DELETE
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    

# service/author/{AUTHOR_ID}/posts/
class CreatePostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # GET: get_queryset is called after a GET command
    def get_queryset(self):
        request_author_id = self.kwargs['author_id']
        print(request_author_id)
        # TODO: allow friends to view the post too
        if (self.request.user.id == request_author_id):
            queryset = Post.objects.filter(author=mainModels.Author.objects.get(id=self.request.user.id))
        else:
            queryset = Post.objects.filter(
                author=mainModels.Author.objects.get(id=request_author_id),
                visibility='PUBLIC'
            )

        return queryset

    # POST: perform_create is called before saving to the database
    def perform_create(self, serializer):
        request_author_id = self.kwargs['author_id']
        if(self.request.user.id == request_author_id):
            serializer.save(author=mainModels.Author.objects.get(id=self.request.user.id))
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
