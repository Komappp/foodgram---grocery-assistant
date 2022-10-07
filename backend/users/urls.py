from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import FollowingAPIView, FollowingViewSet

router = DefaultRouter()
router.register('subscriptions', FollowingViewSet, basename='follows')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:follow_id>/subscribe/',
         FollowingAPIView.as_view()),
]
