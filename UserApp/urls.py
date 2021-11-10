from django.urls import path,include
from django.contrib.auth import views as auth_views
from .import views

app_name='UserApp'
urlpatterns = [

    path('',include('django.contrib.auth.urls')),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/",auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),


]