from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tweet

class TweetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user = serializers.StringRelatedField(read_only=True)
    text = serializers.CharField(max_length=300)
    photo = serializers.ImageField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Tweet.objects.create(**validated_data)