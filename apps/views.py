from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView
from .models import RestaurantReview, Restaurant, Comment, MapUserRestaurant
from .forms import RestaurantForm, RestaurantReviewForm, SearchForm, CommentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from geopy.geocoders import Nominatim
from django.db import IntegrityError
from django.http import JsonResponse


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
