from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.urls import reverse
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField

class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    address = models.TextField(blank=True, default='')
    date = models.DateField(default=date.today)
    location = LocationField(based_fields=['name'], zoom=7, default=Point(1.0, 1.0))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('apps:restaurant_detail', args=[str(self.id)])

    def get_unsuggested_count(self):
        unsuggested_count = MapUserRestaurant.objects.filter(restaurant=self, 
        suggested=False).count()
        return unsuggested_count 


class MapUserRestaurant(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, default=1, on_delete=models.CASCADE)
    suggested = models.BooleanField(default=True)
    visited = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return '{} - review by {}'.format(self.restaurant.name, self.user.username)



class Review(models.Model):
    RATING_CHOICES = (
    (1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
    rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False,
                                              default=3, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        abstract = True


class RestaurantReview(Review):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name="reviews")

    def __str__(self):
        return "{} review".format(self.restaurant.name)

    def get_absolute_url(self):
        return reverse('apps:restaurant_detail', args=[str(self.restaurant.id)])

class Comment(models.Model):
    review = models.ForeignKey(RestaurantReview, on_delete=models.CASCADE, 
                                related_name='comments')
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=datetime.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('apps:restaurant_detail', args=[str(self.review.restaurant.id)])

