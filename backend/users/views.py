from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .models import Following
from .pagination import FollowPagination
from .serializers import FollowingSerializer, FollowingWriteSerializer


User = get_user_model()


class FollowingListAPIView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    pagination_class = FollowPagination

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(follow__user=user)


class FollowingCreateAPIView(APIView):

    def post(self, request, follow_id):
        user = request.user
        data = {
            'follow': follow_id,
            'follower': user.id
        }
        serializer = FollowingWriteSerializer(
            data=data,
            context={'request': request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, follow_id):
        user = request.user
        following = get_object_or_404(
            Following, follow=follow_id, follower=user
        )
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
