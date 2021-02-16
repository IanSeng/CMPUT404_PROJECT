from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from author.serializers import AuthorSerializer, AuthAuthorSerializer

class CreateAuthorView(generics.CreateAPIView):
    """Create a new author in the system"""
    serializer_class = AuthorSerializer

class AuthAuthorView(ObtainAuthToken):
    """Authenticate author in the system"""
    serializer_class = AuthAuthorSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES