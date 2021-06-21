from rest_framework import serializers
from django.db.models import F
from datetime import datetime
from .models import Restaurant, MapUserRestaurant, RestaurantReview, Comment


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.ReadOnlyField(source='id', read_only=True)
    comment_text = serializers.ReadOnlyField(source='text', read_only=True)
    date_created = serializers.ReadOnlyField(source='created_date', read_only=True)
    comment_user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('comment_id', 'comment_text', 'date_created', 'comment_user')

    def get_comment_user(self, obj):
        return obj.user.username


class ReviewSerializer(serializers.ModelSerializer):
    review_id = serializers.ReadOnlyField(source='id', read_only=True)
    review_rating = serializers.ReadOnlyField(source='rating', read_only=True)
    review_text = serializers.CharField(source='comment', read_only=True)
    review_user = serializers.SerializerMethodField()
    date_created = serializers.DateField(source='date', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    visited = serializers.SerializerMethodField()
    recommended = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantReview
        fields = ('review_id', 'review_rating', 'review_text', 
            'review_user', 'date_created', 'comments', 'visited',
            'recommended')

    def get_review_user(self, obj):
        return obj.user.username

    def get_visited(self, obj):
        map_obj = MapUserRestaurant.objects.get(user=obj.user, 
                        restaurant=obj.restaurant)
        return 'Yes' if map_obj.visited else 'No'

    def get_recommended(self, obj):
        map_obj = MapUserRestaurant.objects.get(user=obj.user, 
                        restaurant=obj.restaurant)
        return 'Yes' if map_obj.suggested else 'No'


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.ReadOnlyField(source='id', read_only=True)
    restaurant_name = serializers.CharField(source='name', read_only=True)
    restaurant_address = serializers.CharField(source='address', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        exclude = ('location',)

    def get_reviews(self, obj):
        return obj.restaurantreviewset.all().values('rating','comment', 'user', 'date')