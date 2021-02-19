from django.shortcuts import render, get_object_or_404
from rest_framework import authentication, generics, permissions, status
from main.models import Author
from posts.models import Post
from .models import Inbox
from .serializers import InboxSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# service/author/{AUTHOR_ID}/inbox/
class InboxView(generics.RetrieveDestroyAPIView):
    serializer_class = InboxSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_inbox(self):
        request_author_id = self.kwargs['inboxAuthorID']

        if (self.request.user.id != request_author_id):
            raise ValidationError({"error": ["Not authorized to view this inbox."]})

        return get_object_or_404(Inbox, author=Author.objects.get(id=self.request.user.id))

    # GET: get_queryset is called after a GET command
    def retrieve(self, request, *args, **kwargs):
        inbox = self.get_inbox()
        return Response(InboxSerializer(inbox).data)

    def post(self, request, *args, **kwargs):
        inbox_type = request.data.get('type')
        
        if (inbox_type == 'post'):
            post_id = request.data.get('id')
            request_author_id = self.kwargs['inboxAuthorID']
            # TODO: allow sharing of friend's post
            a_post = get_object_or_404(Post, pk=post_id, visibility=Post.PUBLIC)
            inbox = self.get_inbox()
            inbox.posts.add(a_post)
            inbox.save()
            return Response(f'Shared {post_id} with {request_author_id}', status=status.HTTP_200_OK)