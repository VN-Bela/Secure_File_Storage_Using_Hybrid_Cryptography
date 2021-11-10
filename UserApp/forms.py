from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class UserSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.save()
        if commit:
            user.save()
        return user
