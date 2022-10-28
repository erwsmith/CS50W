from rest_framework import serializers
from .models import Post, Follower

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'body', 'timestamp', 'liked_by')

class FollowerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Follower
        fields = ('user', 'following')