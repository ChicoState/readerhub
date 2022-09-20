"""readerhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app1 import views as app1_views
from personalization import views as personalization_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', app1_views.home),
    path('admin/', admin.site.urls),
    path('join/', app1_views.join),
    path('login/', app1_views.user_login),
    path('logout/', app1_views.user_logout),
    path('personalization/', personalization_views.personalization),
    path('personalization/add_profile/', personalization_views.add_profile),
    path('personalization/edit_profile/<int:id>/', personalization_views.edit_profile),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #needed to save images to static
