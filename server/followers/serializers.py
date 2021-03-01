from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

from main import models
from author.serializers import AuthorProfileSerializer
class FollowersSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    class Meta:
        model = models.Followers
        fields = ('followers',)
        read_only_fields = ()
    
    def get_followers(self, obj):
        context = self.context
        request = context.get("request")
        print(obj.followers.all())
        allFollowers = obj.followers.all()
        data = [AuthorProfileSerializer(obj).data for obj in allFollowers]
        print(data)
        return data
