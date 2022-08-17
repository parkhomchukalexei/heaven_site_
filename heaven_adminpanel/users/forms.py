from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Client

User = get_user_model()

class UserCreationForm(UserCreationForm):

    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete':'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class CreateClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'surname', 'country', 'login_of', 'password_of', 'of_email',
                  'of_password_email', 'paid_account', 'login_of_paid_account','password_of_paid_account',
                  'email_of_paid_account','password_of_email_paid_account','photo', 'telegram_photos_link')


