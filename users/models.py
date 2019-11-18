from django.db import models
from django.contrib.auth.models import User
from .choices import SEX,SEXUALITY,BUST_SIZE,LANGUAGES,APP_LANGUAGES,FIGURE,TRAVEL_TYPES,MEETUP_LOCATIONS
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from location_field.models.spatial import LocationField
from django.contrib.gis.geos import Point
from location_field.models.plain import PlainLocationField
from django.urls import reverse

# Create your models here.

class Discount(models.Model):
    name = models.CharField(max_length=100)

###############################################################################
                                #SERVICES
###############################################################################

# class Services(models.Model):
#     service = models.CharField(max_length=20)

# class AvailableServices(models.Model):
#     service = models.ForeignKey(Services,on_delete=models.CASCADE)
#     service_fee = models.DecimalField(decimal_places=0,max_digits=10)

###############################################################################
                                #DAYS
###############################################################################

class Day(models.Model):
    day = models.CharField(max_length=50,unique=True)
    position = models.IntegerField()

    class Meta:
        ordering = ('-position',)

    def __str__(self):
        return self.day

class AvailableDay(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    day = models.OneToOneField(Day,on_delete=models.CASCADE,unique=True)
    available_time_from = models.TimeField()
    available_time_to = models.TimeField()

    def __str__(self):
            return '{}--{} schedule'.format(self.user,self.day)

###############################################################################
                                #PROFILE
###############################################################################

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    forename = models.CharField(max_length=100)
    city = models.CharField(max_length=255, verbose_name='city based in')
    location = LocationField(based_fields=['city'], zoom=7, default=Point(1.0, 1.0))
    latitude = models.DecimalField(max_digits=10, decimal_places=6,default=0.000001)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,default=0.000001)
    claim = models.CharField(max_length=100)
    phonenumber  = models.CharField(max_length=20)
    app_usage = models.BooleanField(default=False, verbose_name='would you love to use the app')
    sex = models.CharField(choices=SEX,max_length=100)
    sexuality = models.CharField(choices=SEXUALITY,max_length=100, verbose_name='your sexuality')
    birthday = models.DateField(blank=True,null=True)
    figure = models.CharField(choices=FIGURE,max_length=100)
    height = models.PositiveIntegerField(default=0)
    bust_size  = models.CharField(choices=BUST_SIZE,max_length=100)
    languages = models.CharField(choices=LANGUAGES,max_length=100, verbose_name='spoken languages')
    app_language = models.CharField(choices=APP_LANGUAGES,max_length=100)
    intrests = models.CharField(max_length=100, verbose_name='your intrests')
    best_food = models.CharField(max_length=100)
    drinks = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    dress_style = models.CharField(max_length=100)
    upfront_booking = models.PositiveIntegerField(default=0)
    minimum_booking = models.PositiveIntegerField(default=0)
    custom_travel_from_price = models.PositiveIntegerField(default=0)
    price = models.IntegerField(default=0)
    scent = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    upfront_booking_for_travels = models.PositiveIntegerField(default=0)
    minimum_booking_for_travels = models.PositiveIntegerField(default=0)
    meetup_location = MultiSelectField(choices=MEETUP_LOCATIONS,max_length=100)
    description  = models.CharField(max_length=100, verbose_name='brief description')
    booking_notes = models.CharField(max_length=100)
    travel_types = MultiSelectField(choices=TRAVEL_TYPES,max_length=100)
    adult = models.BooleanField(default=False, verbose_name='are you over 18years of age?')
    views = models.PositiveIntegerField(default=0 , verbose_name='number of views')
    profile_pic = models.ImageField(default='default.jpg', upload_to = 'profile_pics')

    def save(self, *args, **kwargs):
        self.latitude  = self.location.y
        self.longitude = self.location.x   
        super(Profile, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def get_absolute_url(self):
        return reverse('users:user_public_profile', kwargs={'user_username': self.user.username})

    def __str__(self):
        return '{} profile location : {}'.format(self.user.username,self.city)



###############################################################################
                                #ELSE
###############################################################################
