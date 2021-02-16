from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    #TODO: need to update 'author' to return key-values pairs
    # type, id, host, displayName, url and github
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Post
        fields = (
            'type', 'title', 'id', 'source', 'origin', 
            'description', 'content_type', 'content',
            'author', 'count', 'size', 'published',
            'visibility', 'unlisted'
        )
        read_only_fields = ['type', 'id', 'author']
