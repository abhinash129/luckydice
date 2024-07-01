from django.contrib import admin
from django.urls import path, include
from .views import forgot_password
from . import views

urlpatterns = [
path('', views.home, name="home"),
path('signup', views.signup, name="signup"), 
path('signin', views.signin, name="signin"),
path('signout', views.signout, name="signout"),
path('activate/<uidb64>/<token>', views.activate, name="activate"),
path('forgot_password/', forgot_password, name='forgot_password'),
path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
path('password_reset_sucess', views.password_reset_sucess, name="password_reset_sucess"),

]
