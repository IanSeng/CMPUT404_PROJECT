from rest_framework import serializers
from .models import Inbox
from posts.serializers import PostSerializer

class InboxSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        data = PostSerializer(obj.posts.all(), many=True).data
        return data

    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')