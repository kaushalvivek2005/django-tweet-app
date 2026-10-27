from rest_framework import serializers
from django.contrib.auth.models import User

class TweetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    text = serializers.CharField(max_length=300)
    photo = serializers.ImageField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
