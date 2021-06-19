from django import forms
from django.forms import ModelForm, TextInput, URLInput
from .models import Restaurant, RestaurantReview, Comment
from django.contrib.gis.geos import Point
from location_field.forms.spatial import LocationField


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        exclude = ('date','address')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'location': LocationField(based_fields=['name'],
                             initial=Point(-49.1607606, -22.2876834))
        }

        labels = {
                   'name': 'Name',
                    'location': 'Location'
                    }

class RestaurantReviewForm(ModelForm):
    class Meta:
        model = RestaurantReview
        exclude = ('user', 'date', 'restaurant')


class SearchForm(forms.Form):
    text = forms.CharField(label='Search', 
            help_text='Search by Restaurant Name or Address', 
            max_length=250)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
            

