from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, logout
from django.http import Http404
from django.db.models import Q

#rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework  import permissions
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_302_FOUND
)

User = get_user_model()

from .serializers import TweetSerializer, LikeSerializer, CommentSerializer
from .models import Tweet, Likes, Comments
from .permissions import IsOwnerOrReadOnly

@method_decorator(csrf_exempt, name='dispatch')
class Tweets(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)
    
    def get(self, request):
        tweets = Tweet.objects.all().order_by('-id')
        serializer = TweetSerializer(tweets, many=True)
        return Response({"tweets":serializer.data})

    def post(self, request):
        data = request.data
        serializer = TweetSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response({"Data":serializer.data}, status=HTTP_200_OK)
        return Response({"Data":serializer.errors}, status=HTTP_200_OK)

class TweetEditDeleteUpdate(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tweet = self.get_object(pk)
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_dislike(request):
    try:
        tweet = Tweet.objects.get(id=request.data.get('tweet'))
    except Tweet.DoesNotExist:
        raise Http404
    like = Likes.objects.filter(tweet=tweet, user=request.user)
    if like:
        like.delete()
        return Response({"message":"Disliked", "code":2}, status=HTTP_200_OK)
    else:
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tweet = tweet, user=request.user)
            return Response({"Data":serializer.data}, status=HTTP_200_OK)
        return Response({"Data":serializer.errors}, status=HTTP_200_OK)
    
    return Response({"message":"something wrong."}, status=HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class Comment(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  

    def get_object(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise Http404

    def post(self, request):
        data = request.data
        tweet = self.get_object(request.data.get('tweet'))
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(tweet = tweet, user=self.request.user)
            return Response({"Data":serializer.data}, status=HTTP_200_OK)
        return Response({"Data":serializer.errors}, status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def total_likes(request, tweet_id): 
    likes = Likes.objects.filter(tweet=tweet_id).count()
    return Response({"likes":likes}, status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def total_comments(request, tweet_id): 
    comments = Comments.objects.filter(tweet=tweet_id).count()
    return Response({"comments":comments}, status=HTTP_200_OK)
