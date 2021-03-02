from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from main import models
from followers.serializers import FollowersSerializer


class FollowersView(generics.RetrieveAPIView):
    serializer_class = FollowersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        request_author_id = self.kwargs['id']

        if not self.request.user.adminApproval:
            raise AuthenticationFailed(
                detail={
                    "error": ["User has not been approved by admin"]
                }
            )

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
