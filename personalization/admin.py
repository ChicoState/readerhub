from django.contrib import admin
from .models import Follows
from .models import Critic
from .models import PersonalInfo

#need models to be able to change values, currently only way to asign a user to be a critic
admin.site.register(Follows)
admin.site.register(Critic)
admin.site.register(PersonalInfo)
