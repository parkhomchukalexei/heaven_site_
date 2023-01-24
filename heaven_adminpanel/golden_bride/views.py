import json
from datetime import datetime, date
from time import strftime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from golden_bride.models import GoldenBrideTable, TableData
from golden_bride.serializers import TableSerializer, DataSerializer
from users.models import Client, User
from golden_bride.forms import CreateGoldenBrideTable


# Create your views here.


class GoldenBrideWorkpage(LoginRequiredMixin, View):
    # permission_required = 'onlyfans.view_onlyfanstable'
    template = 'golden_bride_template/workpage.html'

    def get_by_operator_id(self, pk):

        data = json.loads(find())
        final_data = []
        for i in data:
            final_data.append(
                {key: value for key, value in i.items() if value['table']['table_info']['operator'] == int(pk)})
        return json.dumps(list(filter(None, final_data)))

    def days_in_month(self):
        month_list = {'January': 31, 'February': 29, 'March': 31, 'April': 30, 'May': 31, 'June': 30, 'July': 31,
                      'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}

        a = [str(i) for i in range(1, month_list[strftime('%B')] + 1)]
        return a

    def get(self, request):

        if 'Operator' in str(request.user.groups.all()):
            context = {
                'form': json.loads(self.get_by_operator_id(pk=request.user.pk)),
                'month': self.days_in_month(),
            }
            return render(request, self.template, context)

        else:
            context = {
                'form': json.loads(find()),
                'month': self.days_in_month(),
            }
            return render(request, self.template, context)

    def post(self, request):
        data = request.POST
        day = dict(data)['day'][0]
        value = dict(data)['value'][0]
        table_id = dict(data)['table_id'][0]
        table = GoldenBrideTable.objects.filter(id=int(table_id))
        new_data = TableData(
            data=float(value),
            date=datetime(year=2022, month=8, day=int(day)),
            table=table[0]
        )
        new_data.save()

        return redirect('golden_bride_workpage')


def get_id_list():
    data = (int(i.operator.pk) for i in GoldenBrideTable.objects.all())
    return tuple(set(data))


def make_get():
    data = {f'table_{a.id}': {'table':
                                  {'table_info': TableSerializer(a).data,
                                   f'table_data': DataSerializer(TableData.objects.filter(table_id=int(a.id)),
                                                                 many=True).data}
                              }
            for a in
            GoldenBrideTable.objects.prefetch_related('tabledata_set').all()}

    return data


def find():
    data = make_get()
    id_list = get_id_list()
    final_data = []
    for i in id_list:
        final_data.append({key: value for key, value in data.items() if value['table']['table_info']['operator'] == i})
    return json.dumps(final_data)


class CreateNewTable(LoginRequiredMixin, View):
    # permission_required = 'onlyfans.onlyfans_table.can_add'
    template = 'golden_bride_template/create_table.html'

    def get(self, request):
        context = {
            'form': CreateGoldenBrideTable,
        }
        return render(request, self.template, context)

    def post(self, request):
        form = CreateGoldenBrideTable(request.POST)

        month = date(month=int(request.POST['month']), day=1, year=2023)
        account_id = request.POST['account_id']

        if form.is_valid:
            new_table = GoldenBrideTable(
                date=month,
                client=Client.objects.filter(id=int(request.POST['client']))[0],
                operator=User.objects.filter(id=int(request.POST['operator']))[0],
                account_id=account_id,
            )
            new_table.save()
        return redirect('golden_bride_workpage')


class TableViewSet(viewsets.ModelViewSet):
    queryset = GoldenBrideTable.objects.prefetch_related('tabledata_set').all()
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
        return Response({'data': json.dumps(list(filter(None, final_data)))})

    @action(methods=['get'], detail=True, )
    def get_by_operator_id_and_month(self, request, pk):
        data = json.loads(find())
        final_data = []
        print(
            request.args.get())  # Я остановился тут, доделать считывание аргумента, надо передать через ГЕТ запрос правильно
        # month = request['month']
        for i in data:
            final_data.append(
                {key: value for key, value in i.items() if value['table']['table_info']['operator'] == int(pk)
                 and value['table']['table_info']['date'][5:7] == 1})
        return Response({'data': json.dumps(list(filter(None, final_data)))})


class TableDataSet(viewsets.ModelViewSet):
    queryset = TableData.objects.all()
    serializer_class = DataSerializer

    def create(self, request, *args, **kwargs):

        table_data = {"data": request.data['data'], "data_type": str(request.data['data_type']),
                      "table": int(request.data['table']),
                      "date": date(month=10, day=int(request.data['date']), year=2022)}

        serializer = DataSerializer(data=table_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/golde-bride/')
        else:
            print(f"{serializer.errors}")

    def partial_update(self, request, pk=None, *args, **kwargs):

        def get_object(pk):
            return TableData.objects.get(pk=pk)

        td_object = get_object(pk=pk)

        serializer = DataSerializer(td_object, data={'data': request.data['data'], 'date': td_object.date,
                                                     'table': int(td_object.table.pk)})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': 'done'})
        else:
            return Response(serializer.errors)