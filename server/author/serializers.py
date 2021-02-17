from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {
                        'username': {'write_only': True, 'min_length': 3},
                        'password': {'write_only': True, 'min_length': 5}, 
                        }

    def create(self, validated_data):
        return get_user_model().objects.create_author(**validated_data)

class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'type', 'id', 'host', 'displayName', 'url', 'github')

class AuthAuthorSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def validate(self, attributes):
        username = attributes.get('username')
        password = attributes.get('password')

        author = authenticate(
            username=username, 
            password=password,
        )
        if author is not None:
            attributes['user'] = author
          
            return attributes
        else:
            errorMsg = ('Unable to authenticate the user')
            raise serializers.ValidationError(errorMsg, code='authentication')

