from django.urls import path, re_path
from . import views

# namespace
app_name = 'apps'

urlpatterns = [
 # View restaurant list
    path('', views.RestaurantList.as_view(), name='restaurant_list'),

 # View restaurant details, such as /apps/restaurant/1/
    re_path(r'^restaurant/(?P<pk>\d+)/$',
        views.RestaurantDetail.as_view(), name='restaurant_detail'),

 #Create a restaurant, such as: /apps/restaurant/create/
    re_path(r'^restaurant/create/$', views.RestaurantCreate.as_view(),
            name='restaurant_create'),

 # Edit restaurant details, such as: /apps/restaurant/1/edit/
    re_path(r'^restaurant/(?P<pk>\d+)/edit/$',
        views.RestaurantEdit.as_view(), name='restaurant_edit'),

 # Create restaurant review
    re_path(r'^review/create/(?P<restaurant_id>\d+)',
        views.RestaurantReviewCreate.as_view(), name='restaurant_review_create'),

# Create review comment
    re_path(r'^review/(?P<review_id>\d+)/comment',
        views.add_comment_to_review, name='add_comment_to_review'),

# Create review comment
    re_path(r'^restaurant/(?P<pk>\d+)/thumps-down',
        views.thumps_down, name='rate_negative'),

]