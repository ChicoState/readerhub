# pylint: disable=C0114
from django.contrib import admin
from .models import Follows
from .models import Critic
from .models import PersonalInfo
from .models import FavoriteBooks

# Register your models here.
admin.site.register(Follows)
admin.site.register(Critic)
admin.site.register(PersonalInfo)
admin.site.register(FavoriteBooks)
