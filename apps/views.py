from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView
from .models import RestaurantReview, Restaurant #, Dish
from .forms import RestaurantForm, RestaurantReviewForm #, DishForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


class RestaurantList(ListView):

    queryset = Restaurant.objects.all().order_by('-date')
    context_object_name = 'latest_restaurant_list'
    template_name = 'apps/restaurant_list.html'


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

    # Associate form.instance.user with self.request.user
    def form_valid(self, form):
        form.instance.user = self.request.user
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
        form.instance.restaurant = Restaurant.objects.get(id=restaurant_id)
        return super(RestaurantReviewCreate, self).form_valid(form)



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