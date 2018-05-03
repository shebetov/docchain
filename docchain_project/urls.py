"""docchain_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
import main_site.views as main_site_views
import doctors.views as doctors_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', main_site_views.registration),
    path('doctors/', doctors_views.doctors),
    path('appointment/', doctors_views.appointment),
    path('about_organization/', main_site_views.about_organization),
    path('about_docchain/', main_site_views.about_docchain),
    path('contact/', main_site_views.contact),
    path('', main_site_views.home)
]