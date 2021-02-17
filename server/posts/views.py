from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from main import models as mainModels
from .models import Post
from .serializers import PostSerializer


# service/author/{AUTHOR_ID}/posts/{POST_ID}
class UpdatePostView(generics.RetrieveUpdateDestroyAPIView): #mixins.DestroyModelMixin
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # get_queryset is needed for the PUT method
    # returning all posts made by current user because you can only update your own posts
    # def get_queryset(self):
    #     return Post.objects.filter(author=mainModels.Author.objects.get(id=self.request.user.id))

    # returns a post with the matching author_id and pk (post_id)
    def get_post(self):
        pk = self.kwargs.get('')
        request_author_id = self.kwargs['author_id']
        request_post_id = self.kwargs['pk']

        # TODO: allow friends to view the post too
        if (self.request.user.id == request_author_id):
            a_post = get_object_or_404(Post, pk=request_post_id)
        else:
            a_post = get_object_or_404(Post, pk=request_post_id, visibility=Post.PUBLIC)
        return a_post

    # GET the post with the right author_id and post_id
    def retrieve(self, request, *args, **kwargs):
        a_post = self.get_post()
        return Response(PostSerializer(a_post).data)
    
    # DELETE - Only the author of the post can perform the deletion
    def delete(self, request, *args, **kwargs):
        if (self.kwargs['author_id'] == self.request.user.id):
            if self.get_post():
                self.get_post().delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                # Update this
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # POST - update existing post
    def post(self, request, *args, **kwargs):
        if (self.kwargs['author_id'] != self.request.user.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        a_post = self.get_post()
        serializer = PostSerializer(a_post, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, *args, **kwargs):
    #     return self.get_serializer(Post, data=request.data, partial=True)
    


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
    # TODO: only allow user to create post if author id matches?      
    def perform_create(self, serializer):
        request_author_id = self.kwargs['author_id']
        serializer.save(author=mainModels.Author.objects.get(id=self.request.user.id))
