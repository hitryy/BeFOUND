from django.contrib import admin
from .models import Profile, UserAB, AlarmButton, UsedAlarmButton

# Register your models here.
admin.site.register(Profile)
admin.site.register(UserAB)
admin.site.register(AlarmButton)
admin.site.register(UsedAlarmButton)
