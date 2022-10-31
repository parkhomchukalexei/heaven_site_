from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from rest_framework.decorators import action

from .models import OnlyFansTable,TableData
from .forms import CreateOnlyfansTable
from users.models import Client,User
from time import strftime, struct_time
from datetime import datetime, date
from rest_framework.views import APIView, Response
from rest_framework import viewsets
from .serializers import TableSerializer, DataSerializer
import json


class OnlyFansWorkpage(View):

    template = 'onlyfans_template/workpage.html'


    def days_in_month(self):
        month_list = {'January': 31, 'February': 29, 'March': 31, 'April': 30, 'May': 31, 'June': 30, 'July': 31,
        'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}
        #days = [ strftime('%d',i) for i in range(1, month_list[strftime('%B')] + 1)]
        #print(days)

        a = [str(i) for i in range(1, month_list[strftime('%B')] + 1)]
        return a


    def get(self, request):

        context = {
            'form': json.loads(find()),
            'month': self.days_in_month(),
        }
        return render(request, self.template, context)


    def post(self,request):
        data = request.POST
        day = dict(data)['day'][0]
        value = dict(data)['value'][0]
        type = dict(data)['type'][0]
        table_id = dict(data)['table_id'][0]
        table = OnlyFansTable.objects.filter(id=int(table_id))
        new_data = TableData(
            data = float(value), data_type = type,
            date = datetime(year=2022,month=8,day=int(day)),
            table = table[0]
        )
        new_data.save()

        return redirect('onlyfans_workpage')


class CreateNewTable(View):

    template = 'onlyfans_template/create_table.html'

    def get(self, request):
        context = {
            'form': CreateOnlyfansTable,
        }
        return render(request,self.template, context)

    def post(self, request):

        form = CreateOnlyfansTable(request.POST)
        if form.is_valid:
            if request.POST['table_type'] == '0':
                new_table = OnlyFansTable(
                    client=Client.objects.filter(id=int(request.POST['client']))[0],
                    operator=User.objects.filter(id=int(request.POST['operator']))[0])
                new_table.save()
            else:
                new_table = OnlyFansTable(
                    table_type=True,
                   client=Client.objects.filter(id=int(request.POST['client']))[0],
                   operator=User.objects.filter(id=int(request.POST['operator']))[0])
                new_table.save()
        return redirect('onlyfans_workpage')



#class TableAPIView(APIView):
#
#    def get(self, request):
#        all_tables = OnlyFansTable.objects.prefetch_related('tabledata_set').all()
#        return Response({'tables': TableSerializer(all_tables, many=True).data})
#
#    def post(self,request):
#        new_table = OnlyFansTable.objects.create(
#         date=request.data['date'],
#         table_type=request.data['table_type'],
#         client=int(request.data['client_id']),
#         operator=int(request.data['operator_id']))
#        return Response({'new_table': TableSerializer(new_table).data})
#
#    def put(self,request):
#        pass
#
#    def delete(self,request):
#        deleted_table = OnlyFansTable.objects.filter(id=int(request.query_params['table_id']))
#        deleted_table.delete()
#        return Response({'deleted_table': TableSerializer(deleted_table).data})


#class TableDataAPIView(APIView):
#
#    def get(self, request):
#        all_data = TableData.objects.all()
#        return Response({'data': DataSerializer(all_data, many=True).data})
#
#    def post(self,request):
#        print(request)
#        return redirect('onlyfans-workpage')


class TableViewSet(viewsets.ModelViewSet):
    queryset = OnlyFansTable.objects.prefetch_related('tabledata_set').all()
    serializer_class = TableSerializer


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


class TableDataSet(viewsets.ModelViewSet):
    queryset = TableData.objects.all()
    serializer_class = DataSerializer

    def create(self, request, *args, **kwargs):

        print(request.data['date'])
        table_data = {"data": request.data['data'],"data_type":str(request.data['data_type']), "table": int(request.data['table']),
                      "date": date(month = 10, day= int(request.data['date']), year= 2022)}

        serializer = DataSerializer(data=table_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/onlyfans/')
        else: print(f"{serializer.errors}")


    def partial_update(self, request, pk=None, *args, **kwargs):

        def get_object(pk):
            return TableData.objects.get(pk=pk)

        td_object = get_object(pk=pk)

        serializer = DataSerializer(td_object, data={'data': request.data['data'], 'date': td_object.date,
                                                     'data_type': td_object.data_type, 'table': int(td_object.table.pk) })
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'done'})
                #HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/onlyfans/')
        else: print(serializer.errors)










