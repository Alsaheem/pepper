from django.contrib import admin

from users.models import Day,AvailableDay,Discount,Profile

# Register your models here.

admin.site.register(AvailableDay)
admin.site.register(Profile)
admin.site.register(Day)
admin.site.register(Discount)
