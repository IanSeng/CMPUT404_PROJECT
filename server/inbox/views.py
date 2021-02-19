from django.shortcuts import render
from rest_framework import authentication, generics, permissions, status
from main.models import Author
from .models import Inbox
from .serializers import InboxSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# service/author/{AUTHOR_ID}/inbox/
class InboxView(generics.ListCreateAPIView):
    serializer_class = InboxSerializer
    authenticate_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # GET: get_queryset is called after a GET command
    def get_queryset(self):
        request_author_id = self.kwargs['author_id']

        if (self.request.user.id != request_author_id):
            raise ValidationError({"error": ["Not authorized to view this inbox."]})

        queryset = Inbox.objects.filter(author=Author.objects.get(id=self.request.user.id))

        return queryset