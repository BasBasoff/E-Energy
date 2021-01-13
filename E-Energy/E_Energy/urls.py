"""
Definition of urls for E_Energy.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views



urlpatterns = [
    path('', views.home, name='home'),
    path('<int:dev_id>/', views.home, name='home_with_devid'),
    path('entrances/', views.entrances, name='entrances'),
    path('entrances/<int:device>', views.entrances, name='entrances_with_device_id'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls, name='admin'),
    path('^', include('django.contrib.auth.urls'))
]
