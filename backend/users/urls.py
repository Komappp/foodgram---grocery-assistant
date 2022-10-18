from django.urls import include, path
from users.views import FollowingCreateAPIView, FollowingListAPIView

urlpatterns = [
    path('users/subscriptions/', FollowingListAPIView.as_view()),
    path('', include('djoser.urls')),
    path('users/<int:follow_id>/subscribe/',
         FollowingCreateAPIView.as_view()),
]
