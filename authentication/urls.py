from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register_view, name='register'),
    path('api/request-otp', views.request_otp, name='request_otp'),
    path('api/verify-otp', views.verify_otp, name='verify_otp'),
]