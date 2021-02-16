from django.contrib.auth import get_user_model

from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'type', 'id', 'host', 'displayName', 'url', 'github')
        extra_kwargs = {
                        'username': {'write_only': True, 'min_length': 3},
                        'password': {'write_only': True, 'min_length': 5}, 
                        'type': {'read_only': True},
                        'id': {'read_only': True},
                        'host': {'read_only': True},
                        'displayName': {'read_only': True},
                        'url': {'read_only': True},
                        'github': {'read_only': True},
                        }

    def create(self, validated_data):
        return get_user_model().objects.create_author(**validated_data)
