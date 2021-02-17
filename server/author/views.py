from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.exceptions import ValidationError
from author.serializers import AuthorSerializer, AuthAuthorSerializer, AuthorProfileSerializer

from django.contrib.auth import get_user_model
class CreateAuthorView(generics.CreateAPIView):
    """Create a new author in the system"""
    serializer_class = AuthorSerializer

class AuthAuthorView(ObtainAuthToken):
    """Authenticate author in the system"""
    serializer_class = AuthAuthorSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class AuthorProfileView(generics.ListCreateAPIView):
    """G author in the system"""
    http_method_names = ["get", "post"]
    serializer_class = AuthorProfileSerializer
    # authenticate_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        id = self.kwargs['pk']
        try:
            queryset = get_user_model().objects.filter(id=id)
            return queryset
        except:
            raise ValidationError({"error": ["User not found"]})
    