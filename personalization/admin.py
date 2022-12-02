from django.contrib import admin
from .models import Follows, PersonalInfo

# Register your models here.
admin.site.register(Follows)
admin.site.register(PersonalInfo)
