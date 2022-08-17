from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .models import OnlyFansTable,TableData
from .forms import CreateOnlyfansTable
from users.models import Client,User
from time import strftime
from datetime import datetime
from rest_framework.views import APIView, Response
from .serializers import TableSerializer, DataSerializer



class OnlyFansWorkpage(View):

    template = 'onlyfans_template/workpage.html'


    def days_in_month(self):
        month_list = {'January': 31, 'February': 29, 'March': 31, 'April': 30, 'May': 31, 'June': 30, 'July': 31,
        'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}

        return range(1, month_list[strftime('%B')] + 1)


    def get(self, request):

        context = {
            'form': OnlyFansTable.objects.all(),
            'month': self.days_in_month(),
            'data': self.get_data(1),
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


    def get_data(self, table_id):
        data = TableData.objects.filter(table_id=int(table_id))
        new_data = list(data)
        print(new_data)
        sorted_by_id = {}
        for i in range(0, len(new_data)):
            sorted_by_id[i] = (data.filter(table=i))
        return sorted_by_id






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
                    table_type = True,
                   client=Client.objects.filter(id=int(request.POST['client']))[0],
                   operator=User.objects.filter(id=int(request.POST['operator']))[0])
                new_table.save()
        return redirect('onlyfans_workpage')



class TableAPIView(APIView):

    def get(self, request):
        all_tables = OnlyFansTable.objects.all()
        return Response({'tables': TableSerializer(all_tables, many=True).data})



class TableDataAPIView(APIView):

    def get(self, request):
        all_data = TableData.objects.filter(id=int(request.query_params['table_id']))
        return Response({'data': DataSerializer(all_data, many=True).data})






