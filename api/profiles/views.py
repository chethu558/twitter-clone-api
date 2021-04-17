from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, logout
from django.db.models import Q
from django.http import Http404

#rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework  import permissions
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_302_FOUND
)

from api.permissions import IsOwnerOrReadOnly

User = get_user_model()

from api.posts.models import Tweet
from api.posts.serializers import TweetSerializer

from .serializers import ProfileSerializer

@method_decorator(csrf_exempt, name='dispatch')
class Profile(APIView):
    pass

@method_decorator(csrf_exempt, name='dispatch')
class ProfileUpdateDelete(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        user = self.get_object(id)
        posts = TweetSerializer(Tweet.objects.filter(user=user), many=True)
        serializer = ProfileSerializer(user.profile)
        return Response({'profile':serializer.data, 'posts':posts.data})

    def put(self, request, id, format=None):
        user = self.get_object(id)
        serializer = ProfileSerializer(user.profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
