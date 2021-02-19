from rest_framework import serializers
from .models import Inbox
from posts.serializers import PostSerializer
from main import utils

class InboxSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_items(self, obj):
        data = PostSerializer(obj.posts.all(), many=True).data
        return data

    def get_author(self, obj):
        return f"{utils.HOST}/author/{obj.author.id}"

    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')