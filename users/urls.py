from django.urls import path,include
from users.views import UserProfile,UserPublicProfile,ProfileList,HomePage,AboutView,ContactView,locate_me

app_name = 'users'

urlpatterns = [
    path('', HomePage , name='home'),
    path('locate/', locate_me , name='locate'),
    path('about/', AboutView.as_view() , name='about'),
    path('contact/', ContactView.as_view() , name='contact'),
    path('profile/', UserProfile , name='profile'),
    path('allprofiles/', ProfileList , name='profiles'),
    path('<user_username>/', UserPublicProfile , name='user_public_profile'),
]
