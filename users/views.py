from django.shortcuts import render,redirect
from users.forms import ProfileForm,UserUpdateForm
from users.models import Day,AvailableDay,Discount,Profile
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView,TemplateView
from django.conf import settings
from zipcode_locator import get_zipcode_location
from address_locator import get_address_location
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .filters import ProfileFilter
from django.shortcuts import get_object_or_404
# Create your views here.

# zipcode_required_mixin goes here

def HomePage(request):
    # request.session['longitude'] = 12.44553
    # request.session['latitude'] = 4.22478
    if request.method == 'POST':
        zipcode = request.POST.get('zipcode')
        if zipcode != '':
            zipcode_coordinates = get_zipcode_location(zipcode)
            if zipcode_coordinates is not None :
                address = zipcode_coordinates[0]
                latitide = zipcode_coordinates[1]
                longitude = zipcode_coordinates[2]
                # add location variables to session
                request.session['address'] = address
                request.session['longitude'] = longitude
                request.session['latitude'] = latitide
                return redirect('users:profiles')
            else:
                messages.error(request, 'Location cannot be gotten from Zipcode, Try Another')
                return redirect('/')
        else:
            messages.error(request, 'Zipcode cannot be empty')
            return redirect('/')
    # if request.GET.get('action') == 'locate':
    #     auto_get_lat = request.GET.get('longitude')
    #     print(auto_get_lat)
    #     pass
    template_name =  'index.html'
    context = {}
    return render(request,template_name,context)

def locate_me(request):
    if request.method == 'POST':
        auto_get_lat = request.POST.get('latitude')
        auto_get_lon = request.POST.get('longitude')
        print(auto_get_lat)
        request.session['longitude'] = float(auto_get_lon)
        request.session['latitude'] = float(auto_get_lat)
        messages.success(request, 'Your absolute location has been determined  you can now navigate to browse profiles')
        print(request.session['longitude'])
        return redirect('/')

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

@login_required
def UserProfile(request):
    api_key = 'AIzaSyBLHrLLu1EqgDq0kNKAS-j38YeFidGKpWc'
    myschedule = AvailableDay.objects.filter(user=request.user)
    if request.method== 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid:
            data= p_form.save(commit=False)
            city = data.city
            address_coordinates = get_address_location(city)
            if address_coordinates is not None:
                # overrite save method
                latitide = address_coordinates[1]
                longitude = address_coordinates[2]
                location = Point(latitide,longitude)
                data.location = location
                data.save()
            u_form.save()
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context= {
        'u_form':u_form,
        'p_form':p_form,
        'myschedule':myschedule,
        'api_key':api_key
    }
    return render(request,'profile/profile.html',context)


def ProfileList(request):
    # get_session_longitude and latitude 
    try:
        request.session['longitude']
    except KeyError:
        messages.error(request, 'Your absolute location could not be determined')
        messages.error(request, 'Please put in a valid zipcode in the form below to continue')
        return redirect('/')
    latitude = request.session['latitude']
    longitude = request.session['longitude']
    print([latitude,longitude])
    user_location = Point(longitude, latitude, srid=4326)
    profiles = Profile.objects.annotate(distance=Distance('location',user_location)).order_by('distance')
    profile_filter = ProfileFilter(request.GET, queryset=profiles)
    template_name = 'profile/profiles.html'
    context = {'profiles':profiles,'profile_filter': profile_filter}
    return render(request,template_name,context)



def UserPublicProfile(request,user_username):
    user = get_object_or_404(User,username=user_username)
    profile = Profile.objects.get(user=user)
    profile.views =  profile.views +  1
    profile.save()
    schedule = AvailableDay.objects.filter(user=user)
    template_name = 'profile/public_profile.html'
    context = {'userprofile':profile,'user_schedule':schedule,'user':user}
    return render(request,template_name,context)




