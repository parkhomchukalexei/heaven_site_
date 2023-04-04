import json
from datetime import datetime, date
from time import strftime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response

from golden_bride.models import GoldenBrideTable, TableData
from golden_bride.serializers import TableSerializer, DataSerializer
from users.models import Client, User
from golden_bride.forms import CreateGoldenBrideTable
from onlyfans.views import ViewData


# Create your views here.


class GoldenBrideWorkpage(LoginRequiredMixin, View):
    permission_required = 'golden_bride.view_goldenbridetable'
    template = 'golden_bride_template/workpage.html'

    def __init__(self):
        self.data = ViewData(table_object=GoldenBrideTable, table_serializer=TableSerializer, table_data_object=TableData,
                             data_serializer=DataSerializer)

    def create_pagination_object(self, user):

        data = []
        for i in range(1, 13):
            if i < 10:
                month = '0' + str(i)
            else:
                month = str(i)
            if '[Golden Bride] Operator' in str(user.groups.all()):
                data.append(
                    self.data.get_by_operator_id_and_month(pk=user.pk, month=month))
            else:
                data.append(self.data.get_by_month(month=month))
        return data

    def get(self, request):
        if '[Golden Bride] Operator' in str(request.user.groups.all()):
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


class CreateNewTable(LoginRequiredMixin, View):
    permission_required = 'golden_bride.add_goldenbridetable'
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


class TableDataSet(viewsets.ModelViewSet):
    queryset = TableData.objects.all()
    serializer_class = DataSerializer

    def create(self, request, *args, **kwargs):
        if 'page ' in request.META.get('HTTP_REFERER'):
            url = request.META.get('HTTP_REFERER')[int(request.META.get('HTTP_REFERER').find("=")) + 1::]
        else:
            url = '1'
        table_data = {"data": request.data['data'], "data_type": str(request.data['data_type']),
                      "table": int(request.data['table']),
                      "date": date(month=int(url), day=int(request.data['date']), year=2022)}

        serializer = DataSerializer(data=table_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(redirect_to=f'http://127.0.0.1:8000/golden_bride/?page={url}')
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