import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import action

from .forms import CreateClientForm, SetOperator, SetPromotion, SetProjectManager

# Create your views here.
from django.views import View
from users.forms import UserCreationForm
from users.models import Client, User
from rest_framework.views import APIView, Response
from rest_framework import viewsets
from users.serializers import ClientSerializer, PermissionSerializer, UserSerializer


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

    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        client_data = {'name' : request.data['name'], 'surname': request.data['lastname'],
                       'login_of': request.data['onlyfanslogin'], 'password_of': request.data['onlyfanspassword'],
                       'of_email': request.data['onlyfansloginemail'], 'of_password_email': request.data['onlyfanspasswordemail'],
                       'paid_account': bool(request.data['payedaccount']), 'login_of_paid_account': request.data['onlyfanspayedlogin'],
                       'password_of_paid_account': request.data['onlyfanspayedpassword'],
                       'email_of_paid_account': request.data['onlyfanspayedloginemail'],
                       'password_of_email_paid_account': request.data['onlyfanspayedpasswordemail'],
                       'photo': request.data['photo'], 'telegram_photos_link': request.data['telegram'],
                       'managers': list([User.objects.filter(pk= self.request.user.pk).first().pk])}

        serializer = ClientSerializer(data=client_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect('http://127.0.0.1:8000/users/client_list/')
        else: print(f'{serializer.errors}')

    @action(methods=['PATCH'], detail=True)
    def set_manager(self, request, pk, *args, **kwargs):
        current_client = Client.objects.filter(pk = pk).first()
        user_to_add = User.objects.filter(pk= request.data['data']).first()
        current_client.managers.add(user_to_add)
        return Response({'vse zbs': "vse ok"})




class ClientList(LoginRequiredMixin,View):

    template_name = 'client/client_list.html'

    def get(self, request):
        user = self.request.user
        if user.is_superuser:
            client_list = Client.objects.all()
        else:
            client_list = Client.objects.all().filter(managers= user.pk)
        context = {'form': client_list}
        return render(request, self.template_name, context)


class ClientPage(LoginRequiredMixin,View):

    template_name = 'client/client_page.html'

    def get(self, request, client_id):
        client = Client.objects.filter(id=client_id)
        operator_list = SetOperator()
        promotion_list = SetPromotion()
        project_list = SetProjectManager()

        current_operators = Client.objects.get(id=client_id).managers.all().filter(groups__name = "Operator")
        current_promotions = Client.objects.get(id=client_id).managers.all().filter(groups__name = "Рекламщики")
        current_project = Client.objects.get(id=client_id).managers.all().filter(groups__name = "Project manager")


        context = {'form': client[0],
                   'operator': operator_list,
                   'promo': promotion_list,
                   'project': project_list,
                   'current_operators': current_operators,
                   'current_promotions': current_promotions,
                   'current_project': current_project,
                   }
        return render(request, self.template_name, context)



class DeleteClient(LoginRequiredMixin,View):

    def get(self,request, client_id):
        client_to_delete = Client.objects.filter(id=client_id)
        client_to_delete.delete()
        return redirect('client_list')


class PermissionList(APIView):

    def get(self,request):
        user = self.request.user
        serializer = PermissionSerializer(data= {
            "id": user.pk, "first_name": user.username, "user_permissions": user.user_permissions})
        if serializer.is_valid():
            return Response({"permission_list": serializer.validated_data})
        else: print(serializer.errors)


class UserAndClientInfo(APIView):

    def get(self, request):
        operator_list = User.objects.filter(groups__name='Operator')
        client_list = Client.objects.all()

        operator = UserSerializer(operator_list, many=True).data
        client = ClientSerializer(client_list, many=True).data
        response = json.dumps({'operator': operator, 'client': client})
        return Response(data=json.loads(response))
