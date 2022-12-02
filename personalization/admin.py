from django.contrib import admin
from .models import Follows
from .models import Critic

# Register your models here.
admin.site.register(Follows)
admin.site.register(Critic)
