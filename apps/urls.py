from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required

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

 # Create restaurant review
    re_path(r'^review/create/(?P<restaurant_id>\d+)',
        login_required(views.RestaurantReviewCreate.as_view()),
        name='restaurant_review_create'),

# Create review comment
    re_path(r'^review/(?P<review_id>\d+)/comment',
        views.add_comment_to_review, name='add_comment_to_review'),

# Mark thumps down
    re_path(r'^restaurant/(?P<pk>\d+)/thumps-down',
        views.thumps_down, name='rate_negative'),

# Create Restaurant Searchable API
    re_path(r'api/v1/getRestaurants', \
         views.RestaurantAPIView.as_view(), name="get_restaurants"),

# View users list
    re_path(r'^users', login_required(views.UserProfileList.as_view()),
            name='users_list'),

# View users detail
    re_path(r'^user_detail/(?P<pk>\d+)/$', login_required(views.UserDetail.as_view()),
            name='user_detail'),

]