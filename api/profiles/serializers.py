from rest_framework import serializers

from api.accounts.models import Profile

class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.ReadOnlyField(source='user.id')
    avatar = serializers.CharField(required=False, allow_blank=True, max_length=256)
    backgroung_img = serializers.CharField(required=False, allow_blank=True, max_length=256)
    title = serializers.CharField(required=False, allow_blank=True, max_length=256)
    description = serializers.CharField(required=False, allow_blank=True, max_length=256)
    url = serializers.CharField(required=False, allow_blank=True, max_length=256)
    dob = serializers.CharField(required=False, allow_blank=True, max_length=20)
    location = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('content', instance.content)
        instance.save()
        return instance