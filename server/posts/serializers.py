from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('_author')
    def _author(self, obj):
        request = self.context.get('request', None)
        if request:
            author = {
                'type': request.user.type,
                'id': request.user.id,
                'host': request.user.host,
                'displayName': request.user.displayName,
                'url': request.user.url,
                'github': request.user.github
            }
            return author

    class Meta:
        model = Post
        fields = (
            'type', 'title', 'id', 'source', 'origin', 
            'description', 'contentType', 'content',
            'author', 'count', 'size', 'published',
            'visibility', 'unlisted'
        )
        read_only_fields = ['type', 'id', 'author']
