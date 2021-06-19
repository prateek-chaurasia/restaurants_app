from django.contrib import admin
from .models import RestaurantReview, Comment, MapUserRestaurant, Restaurant

admin.site.register(Restaurant)
admin.site.register(Comment)
admin.site.register(RestaurantReview)
admin.site.register(MapUserRestaurant)
