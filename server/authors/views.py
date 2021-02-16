from rest_framework import generics

from authors.serializers import AuthorSerializer

class CreateAuthorView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = AuthorSerializer
