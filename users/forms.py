from django import forms
from users.models import Day,AvailableDay,Discount,Profile
from django.contrib.auth.models import User
from location_field.models.spatial import LocationField
from location_field.models.plain import PlainLocationField
from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim

class ProfileForm(forms.ModelForm):
    city= forms.CharField(widget= forms.TextInput
                           (attrs={'id':'city'}))
    location = LocationField(based_fields=['city'], zoom=7, default=Point(1.0, 1.0))
    class Meta:
        model = Profile
        fields = ['forename','city','location','claim','phonenumber','app_usage','sex','sexuality','birthday','figure','height','bust_size','languages','app_language','intrests','best_food','drinks','occupation','dress_style','upfront_booking','minimum_booking','custom_travel_from_price','price','scent','rating','upfront_booking_for_travels','minimum_booking_for_travels','meetup_location','booking_notes','travel_types','adult','profile_pic']
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
