from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from rest_framework.decorators import action

from users.serializers import ClientSerializer, UserSerializer
from .models import OnlyFansTable, TableData
from .forms import CreateOnlyfansTable
from users.models import Client, User
from users.models import Client, User
from datetime import datetime, date
from rest_framework.views import APIView, Response
from rest_framework import viewsets
from .serializers import TableSerializer, DataSerializer, UserAndClientSerializer, TableCreationSerializer
from django.core.paginator import Paginator
import json


class ViewData:

    def __init__(self, table_object, table_serializer, data_serializer, table_data_object):
        self.table_object = table_object
        self.table_data_object = table_data_object
        self.table_serializer = table_serializer
        self.data_serializer = data_serializer

    def get_id_list(self):

        data = (int(i.operator.pk) for i in self.table_object.objects.all())
        return tuple(set(data))

    def make_get(self):

        data = {f'table_{a.id}': {'table':
                                      {'table_info': self.table_serializer(a).data,
                                       f'table_data': self.data_serializer(
                                           self.table_data_object.objects.filter(table_id=int(a.id)),
                                           many=True).data}
                                  }
                for a in
                self.table_object.objects.prefetch_related('tabledata_set').all()}
        return data

    def find(self):

        data = self.make_get()
        id_list = self.get_id_list()
        final_data = []
        for i in id_list:
            final_data.append(
                {key: value for key, value in data.items() if value['table']['table_info']['operator'] == i})
        return json.dumps(final_data)

    def get_by_operator_id_and_month(self, pk, month):
        data = json.loads(self.find())
        final_data = []
        for i in data:
            final_data.append(
                {key: value for key, value in i.items() if value['table']['table_info']['operator'] == int(pk)
                 and value['table']['table_info']['date'][5:7] == month})
        return list(filter(None, final_data))

    def get_by_month(self, month):
        data = json.loads(self.find())
        final_data = []
        for i in data:
            final_data.append(
                {key: value for key, value in i.items() if value['table']['table_info']['date'][5:7] == month})
        return list(filter(None, final_data))

    def days_in_month(self, month):
        month_list = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31,
                      '8': 31, '9': 30, '10': 31, '11': 30, '12': 31}

        a = [str(i) for i in range(1, month_list[month] + 1)]
        return a


class OnlyFansWorkpage(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'onlyfans.view_onlyfanstable'
    template = 'onlyfans_template/workpage.html'

    def __init__(self):
        self.data = ViewData(table_object=OnlyFansTable, table_data_object=TableData, table_serializer=TableSerializer,
                             data_serializer=DataSerializer)

    def create_pagination_object(self, user):

        data = []
        for i in range(1, 13):
            if i < 10:
                month = '0' + str(i)
            else:
                month = str(i)
            if 'Operator' in str(user.groups.all()):
                data.append(
                    self.data.get_by_operator_id_and_month(pk=user.pk, month=month))
            else:
                data.append(self.data.get_by_month(month=month))
        return data

    def get(self, request):
        if 'Operator' in str(request.user.groups.all()):
            if request.GET.get('page'):
                pagination_page = request.GET.get('page')
            else:
                pagination_page = '1'
            table_list = self.create_pagination_object(user=User.objects.get(pk=request.user.pk))
            paginator = Paginator(table_list, 1)
            page_object = paginator.get_page(pagination_page)
            return render(request, self.template, context={'data': page_object,
                                                           'month': self.data.days_in_month(pagination_page)})

        else:
            if request.GET.get('page'):
                pagination_page = request.GET.get('page')
            else:
                pagination_page = '1'
            table_list = self.create_pagination_object(user=User.objects.get(pk=request.user.pk))
            paginator = Paginator(table_list, 1)
            page_object = paginator.get_page(pagination_page)
            return render(request, self.template, context={'data': page_object,
                                                           'month': self.data.days_in_month(pagination_page)})


# class CreateNewTable(LoginRequiredMixin,PermissionRequiredMixin,View):
#     permission_required = 'onlyfans.add_onlyfanstable'
#     template = 'onlyfans_template/create_table.html'
#
#     def get(self, request):
#         context = {
#             'form': CreateOnlyfansTable,
#         }
#         return render(request,self.template, context)
#
#     def post(self, request):
#
#         form = CreateOnlyfansTable(request.POST)
#
#         month = date(month = int(request.POST['month']), day=1, year= 2023)
#
#         if form.is_valid:
#             if request.POST['table_type'] == '0':
#                 new_table = OnlyFansTable(
#                     date = month,
#                     client=Client.objects.filter(id=int(request.POST['client']))[0],
#                     operator=User.objects.filter(id=int(request.POST['operator']))[0])
#                 new_table.save()
#             else:
#                 new_table = OnlyFansTable(
#                     date = month,
#                     table_type=True,
#                     client=Client.objects.filter(id=int(request.POST['client']))[0],
#                     operator=User.objects.filter(id=int(request.POST['operator']))[0])
#                 new_table.save()
#
#         return redirect(f'http://127.0.0.1:8000/onlyfans/?page=1')
#
#


'''
class TableViewSet(viewsets.ModelViewSet):
    queryset = OnlyFansTable.objects.prefetch_related('tabledata_set').all()
    serializer_class = TableSerializer

    @action(methods=['GET'], detail=True)
    def get_by_operator_id(self, request, pk):
        data = json.loads(find())
        final_data = []
        for i in data:
            final_data.append(
                {key: value for key, value in i.items() if value['table']['table_info']['operator'] == int(pk)})
        return Response({'data': json.dumps(list(filter(None, final_data)))})

    @action(methods=['GET'], detail=True)
    def get_by_client_id(self, request, pk):
        print(pk)
        data = json.loads(find())
        final_data = []
        for i in data:
            final_data.append(
                {key: value for key, value in i.items() if value['table']['table_info']['client'] == int(pk)})
        return Response({'data' : json.dumps(list(filter(None, final_data)))})

    @action(methods=['get'], detail=True,)
    def get_by_operator_id_and_month(self, request, pk):
        data = json.loads(find())
        final_data = []
        print(request.args.get()) # Я остановился тут, доделать считывание аргумента, надо передать через ГЕТ запрос правильно
        #month = request['month']
        for i in data:
            final_data.append(
                {key: value for key, value in i.items() if value['table']['table_info']['operator'] == int(pk)
                 and value['table']['table_info']['date'][5:7] == 1})
        return Response({'data': json.dumps(list(filter(None, final_data)))})


def get_id_list():

    data = (int(i.operator.pk) for i in OnlyFansTable.objects.all())
    return tuple(set(data))


def make_get():

    data = {f'table_{a.id}': {'table':
                                  {'table_info': TableSerializer(a).data,
                                   f'table_data': DataSerializer(TableData.objects.filter(table_id = int(a.id)), many=True).data}
                              }
                 for a in
            OnlyFansTable.objects.prefetch_related('tabledata_set').all()}

    return data


def find():

    data = make_get()
    id_list = get_id_list()
    final_data = []
    for i in id_list:
        final_data.append({ key: value for key,value in data.items() if value['table']['table_info']['operator'] == i })
    return json.dumps(final_data)


'''


class TableDataSet(viewsets.ModelViewSet):
    queryset = TableData.objects.all()
    serializer_class = DataSerializer

    def create(self, request, *args, **kwargs):
        # if 'page ' in request.META.get('HTTP_REFERER'):
        #     url = request.META.get('HTTP_REFERER')[int(request.META.get('HTTP_REFERER').find("=")) + 1::]
        # else:
        #     url = '1'
        # print(request.data)
        # Тут мы получаем значение page= и цифру с которой было запрос что бы редиректнуть на эту же страницу
        # пофиксить тут хуйню с датой

        data = request.data['data']
        if ',' in data:
            data = float(data.replace(",", "."))

        table_data = {"data": data, "data_type": "OP", "table": int(request.data['tableId']),
                      "date": date(month=int(1), day=int(request.data['date']), year=2023)}

        serializer = DataSerializer(data=table_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(f"{serializer.errors}")

    def partial_update(self, request, pk=None, *args, **kwargs):

        def get_object(pk):
            return TableData.objects.get(pk=pk)

        td_object = get_object(pk=pk)

        serializer = DataSerializer(td_object, data={'data': request.data['data'], 'date': td_object.date,
                                                     'data_type': td_object.data_type,
                                                     'table': int(td_object.table.pk)})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': 'done'})
        else:
            return Response(serializer.errors)


'''
class Test:

    def get_json_from_base(self):
        table_list = OnlyFansTable.objects.prefetch_related('tabledata_set').filter(operator=3)
        serializer = TableSerializer
        for i in table_list:
            #print(json.dumps(serializer(i).data))
        #print(serializer(table_list[0]).data)

#{client_name: 'Elena', table_type: 'OP',  'day_1': 1}A


a = Test()

a.get_json_from_base()

'''


class TableView(viewsets.ModelViewSet):
    queryset = OnlyFansTable.objects.all()
    serializer_class = TableSerializer

    def list(self, request):

        queryset = OnlyFansTable.objects.prefetch_related('tabledata_set').all().order_by('-date')
        serializer_class = TableSerializer

        user_group = request.user.groups.all()

        if request.user.is_staff:
            month = request.query_params['month']
            table_list = OnlyFansTable.objects.prefetch_related('tabledata_set').filter(date=f'2023-{month}-01')
            data = json.dumps(serializer_class(table_list, many=True).data)
            return Response(json.loads(data))

        if user_group.filter(name='Operator'):
            table_list = OnlyFansTable.objects.prefetch_related('tabledata_set').filter(operator=int(request.user.pk),
                                                                                        date=datetime(year=2023, day=1,
                                                                                                      month=int(
                                                                                                          request.query_params.get(
                                                                                                              "month"))))

            data = json.dumps(serializer_class(table_list, many=True).data)
            return Response(json.loads(data))

    def create(self, request, *args, **kwargs):

        serializer_class = TableCreationSerializer

        full_date = date(month=int(request.data['month']), day=1, year=2023)
        client = int(request.data['client'])
        operator = int(request.data['operator'])
        table_type = request.data['tableType']

        data = {'date': full_date, 'client': client, 'operator': operator, 'table_type': table_type}

        new_table = serializer_class(data=data)
        if new_table.is_valid():
            new_table.save()
            return Response(new_table.data)
        else:
            return new_table.errors

