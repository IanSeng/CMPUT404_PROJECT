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
        extra_kwargs = {   
                        'username': {'read_only': True},
                        'id': {'read_only': True},
                        'type': {'read_only': True},
                        'host': {'read_only': True},
                        'url': {'read_only': True}, 
                        'github': {'required': False}, 
                        'displayName': {'required': False}, 
                        }
                        
    def update(self, instance, validated_data):
        profileAuthor = instance.id
        authenticatedAuthor = self.context['request'].user.id

        if profileAuthor != authenticatedAuthor:
            raise serializers.ValidationError({"error": "You dont have permission for edit this profile."})

        author = super().update(instance, validated_data)

        return author

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
            request=self.context.get('request'),
            username=username, 
            password=password,
        )
        if not author:
            raise serializers.ValidationError({"error": "Unable to authenticate with provided credentials"})

        attributes['user'] = author
        return attributes
        

