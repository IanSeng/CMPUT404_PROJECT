from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('_author')
    id = serializers.SerializerMethodField('_id')

    def _author(self, obj):
        request = self.context.get('request', None)
        if request:
            author = {
                'type': request.user.type,
                'id': request.user.get_id_url(),
                'host': request.user.host,
                'displayName': request.user.displayName,
                'url': request.user.url,
                'github': request.user.github
            }
            return author
    
    def _id(self, obj):
        return obj.get_id_url()

    class Meta:
        model = Post
        fields = (
            'type', 'title', 'id', 'source', 'origin', 
            'description', 'contentType', 'content',
            'author', 'count', 'size', 'published',
            'visibility', 'unlisted'
        )
        read_only_fields = ['type', 'id', 'author']
