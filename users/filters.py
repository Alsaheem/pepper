from django.contrib.auth.models import User
from .models import Profile
import django_filters

class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['sex', 'meetup_location', 'sexuality', 'languages']


