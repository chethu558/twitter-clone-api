from rest_framework import serializers

from .models import Tweet


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