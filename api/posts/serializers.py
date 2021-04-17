from rest_framework import serializers

from .models import Tweet, Likes, Comments


class TweetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.ReadOnlyField(source='user.id')
    tweet = serializers.CharField(required=True, allow_blank=False, max_length=256)

    def create(self, validated_data):
        return Tweet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tweet = validated_data.get('content', instance.content)
        instance.save()
        return instance

class LikeSerializer(serializers.Serializer):
    tweet = serializers.ReadOnlyField(source='tweet.id')
    user = serializers.ReadOnlyField(source='user.id')

    def create(self, validated_data):
        return Likes.objects.create(**validated_data)



class CommentSerializer(serializers.Serializer):
    tweet = serializers.ReadOnlyField(source='tweet.id')
    user = serializers.ReadOnlyField(source='user.id')
    comment = serializers.CharField(required=True, allow_blank=False, max_length=256)

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)