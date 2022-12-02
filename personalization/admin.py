from django.contrib import admin
from .models import Follows
from .models import Critic
from .models import PersonalInfo

# Register your models here.
admin.site.register(Follows)
admin.site.register(Critic)
admin.site.register(PersonalInfo)
