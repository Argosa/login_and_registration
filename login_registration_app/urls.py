from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_registration', views.process_registration),
    path('login', views.process_login),
    path('success', views.success),
    path('logout', views.logout),
]