from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import generics, permissions, status

from django.contrib.auth import get_user_model

from main import models
from followers.serializers import FollowersSerializer, FollowersModificationSerializer
from author.serializers import AuthorProfileSerializer


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
        self.requestAuthorId = self.kwargs['id']
        self.requestForeignAuthorId = self.kwargs['foreignId']
        
        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})

        try:
            self.author = models.Author.objects.get(id=self.requestAuthorId)
            self.foreignAuthor = models.Author.objects.get(id=self.requestForeignAuthorId)
                  
            return models.Followers.objects.filter(author=self.requestAuthorId)

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.get_serializer(instance, data=request.data, partial=True)
        
        if (self.requestAuthorId == self.requestForeignAuthorId):
            return Response({
                'error': ['you cannot follow yourself']}, status=status.HTTP_400_BAD_REQUEST)
        elif (not self.request.user.adminApproval):
            raise AuthenticationFailed(
                detail={"error": ["User has not been approved by admin"]})
        elif (self.requestForeignAuthorId is not request.user.id):
           return Response({
                'error': ['this is not your account, you cannot follow this author']}, status=status.HTTP_403_FORBIDDEN) 
        
        authorObj = models.Author.objects.get(id=self.requestAuthorId)
        author = models.Followers.objects.get(author=authorObj)
        foreignAuthor = models.Author.objects.get(id=self.requestForeignAuthorId)

        author.followers.add(foreignAuthor)
        author.save()
        
        return Response({
            'status': True,
            'author':  self.author.id,
            'follower': self.foreignAuthor.id,
        })