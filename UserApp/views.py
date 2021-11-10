from django.shortcuts import render


from django.urls import reverse_lazy
from django.views import generic
from .forms import UserSignupForm
from .models import User


# Create your views here.


class SignUpView(generic.CreateView):
    form_class = UserSignupForm
    model = User
    success_url = reverse_lazy('UserApp:login')
    template_name = 'registration/signup.html'
