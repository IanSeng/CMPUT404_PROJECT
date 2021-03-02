from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from main import models
from followers.serializers import FollowersSerializer, FollowersModificationSerializer


class FollowersView(generics.RetrieveAPIView):
    serializer_class = FollowersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        request_author_id = self.kwargs['id']

        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})

        try:
            return models.Followers.objects.filter(author=request_author_id)
        except:
            raise ValidationError({"error": ["User not found"]})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'type': 'followers',
            'items': serializer.data['followers'],
        })

class FollowersModificationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FollowersModificationSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_object(self):
        requestAuthorId = self.kwargs['id']
        requestForeignAuthorId = self.kwargs['foreignId']
        
        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})

        try:
            self.author = models.Author.objects.get(id=requestAuthorId)
            self.foreignAuthor = models.Author.objects.get(id=requestForeignAuthorId)
                  
            return models.Followers.objects.filter(author=requestAuthorId)

        except:
            raise ValidationError({"error": ["User not found"]})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': self.foreignAuthor in serializer.data['followers'],
            'author':  self.author.id,
            'follower': self.foreignAuthor.id,
        })