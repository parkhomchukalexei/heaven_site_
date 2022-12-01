from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from .forms import CreateClientForm

# Create your views here.
from django.views import View
from users.forms import UserCreationForm
from users.models import Client
from rest_framework.views import APIView, Response
from rest_framework import viewsets
from users.serializers import ClientSerializer


class Register(View):

    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class CreateClient(LoginRequiredMixin,View):
    template_name = 'client/create_client.html'

    def get(self, request):
        form = CreateClientForm()
        context = {'form': form}
        return render(request, self.template_name, context)


class ClientAPI(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        client_data = {'name' : request.data['name'], 'surname': request.data['lastname'],
                       'login_of': request.data['onlyfanslogin'], 'password_of': request.data['onlyfanspassword'],
                       'of_email': request.data['onlyfansloginemail'], 'of_password_email': request.data['onlyfanspasswordemail'],
                       'paid_account': bool(request.data['payedaccount']), 'login_of_paid_account': request.data['onlyfanspayedlogin'],
                       'password_of_paid_account': request.data['onlyfanspayedpassword'],
                       'email_of_paid_account': request.data['onlyfanspayedloginemail'],
                       'password_of_email_paid_account': request.data['onlyfanspayedpasswordemail'],
                       'photo': request.data['photo'], 'telegram_photos_link': request.data['telegram']}

        serializer = ClientSerializer(data=client_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(redirect_to='../../users/client_list/')
        else: print(f'{serializer.errors}')



class ClientList(LoginRequiredMixin,View):

    template_name = 'client/client_list.html'

    def get(self, request):
        client_list = Client.objects.all()
        context = {'form': client_list}
        return render(request, self.template_name, context)


class ClientPage(LoginRequiredMixin,View):

    template_name = 'client/client_page.html'

    def get(self, request, client_id):
        client = Client.objects.filter(id=client_id)
        context = {'form': client[0]}
        return render(request, self.template_name, context)


class DeleteClient(LoginRequiredMixin,View):

    def get(self,request, client_id):
        client_to_delete = Client.objects.filter(id=client_id)
        client_to_delete.delete()
        return redirect('client_list')









