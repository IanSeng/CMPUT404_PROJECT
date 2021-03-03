from rest_framework import serializers
from .models import Post, Category
from author.serializers import AuthorProfileSerializer

class PostSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    def get_author(self, obj):
        author = AuthorProfileSerializer(obj.author).data
        return author
    
    def get_id(self, obj):
        return obj.get_id_url()

    def get_categories(self, obj):
        return obj.categories.values_list('category', flat=True)

    class Meta:
        model = Post
        fields = (
            'type', 'title', 'id', 'source', 'origin', 
            'description', 'contentType', 'content',
            'author', 'count', 'size', 'published',
            'visibility', 'unlisted', 'categories'
        )
        read_only_fields = ['type', 'id', 'author']
