from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView
from .models import RestaurantReview, Restaurant, Comment, MapUserRestaurant
from .forms import RestaurantForm, RestaurantReviewForm, SearchForm, CommentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from geopy.geocoders import Nominatim
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from .serializers import RestaurantSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from .helpers.api_utils import is_param_valid_client_api
from datetime import datetime
from dateutil.relativedelta import relativedelta

DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0

# API ERROR MSGS
INVALID_JSON_ERR = "Invalid Json Supplied"
GENERIC_EXCEPTION = "Unknown Exception Occured"
api_name = 'get_restaurants'


def get_limit_offset(request):
    limit = int(request.data.get('limit', DEFAULT_LIMIT))
    offset = int(request.data.get('offset',  DEFAULT_OFFSET))
    return limit, offset

class RestaurantList(ListView):

    queryset = Restaurant.objects.all().order_by('-date')
    # context_object_name = 'latest_restaurant_list'
    template_name = 'apps/restaurant_list.html'

    def get_context_data(self, **kwargs):
        context = super(RestaurantList, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        context['search_string'] = ''
        return context

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)
        search_string = request.POST.get('text')
        no_result = ""
        restaurant_list = self.get_queryset().filter(name__icontains=search_string)
        if restaurant_list.count() < 1:
            no_result = "No result found."
        return render(request, 
                    self.template_name, 
                    {'latest_restaurant_list': restaurant_list, 
                    'search_string': search_string,
                    'no_result': no_result,
                    'form': form })



class RestaurantDetail(DetailView):
    model = Restaurant
    template_name = 'apps/restaurant_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        context['RATING_CHOICES'] = RestaurantReview.RATING_CHOICES
        return context


class RestaurantCreate(CreateView):
    model = Restaurant
    template_name = 'apps/form.html'
    form_class = RestaurantForm

    def get_context_data(self, **kwargs):
        context = super(RestaurantCreate, self).get_context_data(**kwargs)
        context['form_heading'] = 'Add Restaurant'
        return context

    # Associate form.instance.user with self.request.user
    def form_valid(self, form):
        geolocator = Nominatim(user_agent="Restaurant App")
        location = geolocator.reverse(self.request.POST.get('location'))
        form.instance.address = location.address
        return super(RestaurantCreate, self).form_valid(form)


class RestaurantEdit(UpdateView):
    model = Restaurant
    template_name = 'apps/form.html'
    form_class = RestaurantForm

class RestaurantReviewCreate(CreateView):
    model = RestaurantReview
    template_name = 'apps/form.html'
    form_class = RestaurantReviewForm

    # Associate form.instance.user with self.request.user
    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data(**self.kwargs)
        restaurant_id = context.get('restaurant_id')
        restaurant_obj = Restaurant.objects.get(id=restaurant_id)
        form.instance.restaurant = restaurant_obj
        visited = self.request.POST.get('visited')
        try:
            MapUserRestaurant.objects.create(
                user = self.request.user,
                restaurant = restaurant_obj,
                visited = True if visited == 'true' else False
            )
        except IntegrityError as ie:
            print("Review already posted by this user")
        except Exception as e:
            print("Error | Mapping was not saved.")
        return super(RestaurantReviewCreate, self).form_valid(form)


def add_comment_to_review(request, review_id):
    review = get_object_or_404(RestaurantReview, pk=review_id)
    if request.method == "POST":
        text = request.POST.get('text')
        try:
            Comment.objects.create(text=text, 
            review=review,
            user=request.user)
        except Exception as e:
            print("Comment not saved")
        return redirect('apps:restaurant_detail', pk=review.restaurant.id)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



def thumps_down(request, pk):
    restaurant_obj = Restaurant.objects.get(pk=pk)
    map_obj = MapUserRestaurant.objects.get(user=request.user,
                restaurant=restaurant_obj)
    if request.method == "POST":
        map_obj.suggested = False
        map_obj.save()
        return JsonResponse({'success': "You have unliked the restaurant"})
    else:
        return JsonResponse({'error': "Some error Occured"})


class RestaurantAPIView(APIView):
    """
    This class will accept filters from client, and returns all the restaurants,
    reviews and comments, it will also allow a search parameter with the name of 
    the restaurant.
    """
    permission_classes = (IsAuthenticated,) 
    serializer_class = RestaurantSerializer
    http_method_names = ['get']

    def get(self, request):
        """
        It recieves only GET request.
        will return available restaurants on the basis of query_params
        or all the restaurants data available in DB.
        query params:
        'limt': int
        'offset': int
        'restaurant_id': 'str' comma seperated restaurant_ids as string
        'review_start_date': 'str' YYYY-MM-DD format expected
        'review_end_date': 'str' YYYY-MM-DD format expected
        'review_rating' : 'str' value from 1 to 5 expected will 
                            return response where review rating is greater than value
        'recommended': 'str' 'Yes' or 'No' expected
        """
        default_start_date = '2000-01-01'
        one_month_later_date = datetime.today() + relativedelta(months=1)
        default_end_date = datetime.strftime(one_month_later_date, '%Y-%m-%d')
        try:
            
            try:
                error_dict = is_param_valid_client_api(request, api_name)
                if error_dict:
                    print(error_dict.get('error'))
                    return Response(error_dict,
                                    status=status.HTTP_400_BAD_REQUEST)
            except (AttributeError, ParseError):
                print(INVALID_JSON_ERR+" {}".format(
                    self.request.data))
                return Response(
                    {"error": INVALID_JSON_ERR},
                    status=status.HTTP_400_BAD_REQUEST
                )

            limit, offset = get_limit_offset(request)
            

            res_ids = request.GET.get('restaurant_id', '').split(',')
            res_ids = [int(k.strip()) if k else '' for k in res_ids]

            start_date = request.GET.get('review_start_date', default_start_date)
            end_date = request.GET.get('review_end_date', default_end_date)
            recommended = request.GET.get('recommended', '')
            
            review_rating = request.GET.get('review_rating', '')

            restaurant_ids = []
            cache_key = 'all_data'
            query ={}

            if recommended:
                if recommended == 'Yes':
                    suggested=True
                elif recommended == 'No':
                    suggested=False

                map_res_ids = MapUserRestaurant.objects.filter(suggested=suggested).values_list('restaurant__id', flat=True)
                res_ids.extend(map_res_ids)
                cache_key = cache_key + request.GET.get('recommended', '')

            if not '' in res_ids and len(res_ids) > 0:
                cache_key = cache_key + request.GET.get('restaurant_id', '')
                query.update({'restaurant__id__in': res_ids})
            
            
            if start_date != default_start_date or end_date != default_end_date:
                query.update({'date__range': (start_date, end_date)})
                cache_key = cache_key + start_date + end_date

            if review_rating:
                query.update({'rating__gte': int(review_rating)})
                cache_key = cache_key + review_rating

            if query:
                review_res_ids = RestaurantReview.objects.filter(**query).order_by('date').values_list('restaurant__id', flat=True)

                restaurant_ids.extend(review_res_ids)

            if restaurant_ids:
                restaurants = Restaurant.objects.filter(id__in=restaurant_ids)
            elif cache_key == 'all_data':
                restaurants = Restaurant.objects.all()
            elif not restaurant_ids and cache_key != 'all_data':
                restaurants = Restaurant.objects.filter(id__in=[-1])

            serializer = RestaurantSerializer(restaurants, many=True)
            restaurants_data = serializer.data
            
            total_count = 0
            if restaurants_data:
                total_count = len(restaurants_data)
                restaurants_data = restaurants_data[offset:offset + limit]
            data = restaurants_data
                
            resp = {
                "error": False,
                "result": data,
                "total_count": total_count,
                "limit": limit,
            }
            print("Restaurants Sucessfully Returned")
            return Response(resp, status=status.HTTP_200_OK)
        except:
            print("Some Exception Occured")
            return Response({"error": GENERIC_EXCEPTION},
                            status=status.HTTP_400_BAD_REQUEST)