from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    #TODO: need to update author to return key-values pairs
    # type, id, host, displayName, url and github
    author = serializers.ReadOnlyField(source='author.id')
    author_name = serializers.ReadOnlyField(source='author.display_name')

    class Meta:
        model = Post
        fields = (
            'author_name', # included author_name for debugging purposes only
            'type', 'title', 'id', 'source', 'origin', 
            'description', 'content_type', 'content',
            'author', 'count', 'size', 'published',
            'visibility', 'unlisted'
        )
