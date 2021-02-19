from django.shortcuts import render, get_object_or_404
from rest_framework import authentication, generics, permissions, status
from main.models import Author
from posts.models import Post
from .models import Inbox
from .serializers import InboxSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

# service/author/{AUTHOR_ID}/inbox/
class InboxView(APIView):
    serializer_class = InboxSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_inbox(self):
        request_author_id = self.kwargs['author_id']

        if (self.request.user.id != request_author_id):
            raise ValidationError({"error": ["Not authorized for this inbox."]})

        return get_object_or_404(Inbox, author=Author.objects.get(id=self.request.user.id))

    # GET: get Inbox of an user
    def get(self, request, *args, **kwargs):
        inbox = self.get_inbox()
        return Response(InboxSerializer(inbox).data)

    # POST: send a Post, Like or Follow to Inbox
    def post(self, request, *args, **kwargs):
        inbox_type = request.data.get('type')

        # TODO: send Like and Follow
        if (inbox_type == 'post'):
            post_id = request.data.get('id')
            request_author_id = self.kwargs['author_id']
            # TODO: allow sharing of friend's post
            a_post = get_object_or_404(Post, pk=post_id, visibility=Post.PUBLIC)
            inbox = self.get_inbox()
            inbox.posts.add(a_post)
            inbox.save()
            return Response(f'Shared {post_id} with {request_author_id}', status=status.HTTP_200_OK)

    # DELETE: Clear the inbox
    def delete(self, request, *args, **kwargs):
        inbox = self.get_inbox()
        inbox.posts.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
