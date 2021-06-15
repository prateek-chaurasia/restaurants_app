from django.forms import ModelForm,  TextInput, URLInput, ClearableFileInput
from .models import Restaurant, RestaurantReview #, Dish


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        exclude = ('user', 'date',)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'telephone': TextInput(attrs={'class': 'form-control'}),
            'url': URLInput(attrs={'class': 'form-control'}),
        }

        labels = {
                   'name': 'name',
                   'address': 'address',
                   'telephone': 'telephone',
                   'url': 'website',
                        }

class RestaurantReviewForm(ModelForm):
    class Meta:
        model = RestaurantReview
        exclude = ('user', 'date', 'restaurant')
