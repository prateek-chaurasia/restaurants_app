from django import forms
from django.forms import ModelForm, TextInput, URLInput, DateField
from .models import Restaurant, RestaurantReview, Comment, Profile
from django.contrib.gis.geos import Point
from location_field.forms.spatial import LocationField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mobile_number', 'birth_date', 'hometown')
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d',
                        attrs={'placeholder':'YYYY-MM-DD'})
        }

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    first_name = forms.CharField(label='Enter first name', max_length=200)
    last_name = forms.CharField(label='Enter last name', max_length=200)
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
            

