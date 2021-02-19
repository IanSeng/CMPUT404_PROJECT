from django.shortcuts import render, get_object_or_404
from rest_framework import authentication, generics, permissions, status
from main.models import Author
from posts.models import Post
from posts.serializers import PostSerializer
from .models import Inbox
from .serializers import InboxSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# service/author/{AUTHOR_ID}/inbox/
class InboxView(generics.RetrieveDestroyAPIView):
    serializer_class = InboxSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # GET: get_queryset is called after a GET command
    def retrieve(self, request, *args, **kwargs):
        request_author_id = self.kwargs['author_id']

        if (self.request.user.id != request_author_id):
            raise ValidationError({"error": ["Not authorized to view this inbox."]})

        inbox = get_object_or_404(Inbox, author=Author.objects.get(id=self.request.user.id))

        return Response(InboxSerializer(inbox).data)

    def post(self, request, *args, **kwargs):
        inbox_type = request.data.get('type')
        request_author_id = self.kwargs['author_id']
        
        if (inbox_type == 'post'):
            post_id = request.data.get('id')
            a_post = get_object_or_404(Post, pk=post_id, visibility=Post.PUBLIC)
            inbox = get_object_or_404(Inbox, author=Author.objects.get(id=self.request.user.id))
            inbox.posts.add(a_post)
            inbox.save()
            return Response('Shared', status=status.HTTP_200_OK)