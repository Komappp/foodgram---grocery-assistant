from api.serializers import RecipeShortSerializer
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Following

User = get_user_model()


class FollowingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='follow.id')
    email = serializers.ReadOnlyField(source='follow.email')
    username = serializers.ReadOnlyField(source='follow.username')
    first_name = serializers.ReadOnlyField(source='follow.first_name')
    last_name = serializers.ReadOnlyField(source='follow.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='follow.recipes.count')

    class Meta:
        model = Following
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Following.objects.filter(
            follower=obj.follower, follow=obj.follow
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.follow)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeShortSerializer(queryset, many=True).data


class FollowingWriteSerializer(serializers.ModelSerializer):

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Following.objects.all(),
                fields=['follower', 'follow'],
                message='Вы уже подписаны на этого автора'
            )
        ]
        model = Following
        fields = '__all__'

    def validate(self, data):
        user = self.context.get('request').user
        follow = data['follow']
        if user == follow:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя"
            )
        return data
