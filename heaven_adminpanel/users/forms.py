from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Client

User = get_user_model()

'''
class CustomUserCreationForm(UserCreationForm):

    email = forms.py.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.py.EmailInput(attrs={'autocomplete':'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
        '''


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class CreateClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'surname', 'country', 'login_of', 'password_of', 'of_email',
                  'of_password_email', 'paid_account', 'login_of_paid_account','password_of_paid_account',
                  'email_of_paid_account','password_of_email_paid_account','photo', 'telegram_photos_link')


class SetOperator(forms.Form):

    operator_list = [(operator.pk, operator.username) for operator in User.objects.filter(groups__name='Operator')]

    valuable_operators = forms.ChoiceField(choices=operator_list, label="Выберите оператора")


class SetPromotion(forms.Form):

    promotion_list = [(promo.pk, promo.username) for promo in User.objects.filter(groups__name='Рекламщики').filter()]

    valuable_promo = forms.ChoiceField(choices=promotion_list, label="Выберите рекламщика")


class SetProjectManager(forms.Form):

    project_manager_list = [(project.pk, project.username) for project
                            in User.objects.filter(groups__name="Project manager")]

    valuable_project_manager = forms.ChoiceField(choices=project_manager_list, label="Выберите проект менеджера")





