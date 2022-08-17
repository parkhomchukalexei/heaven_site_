
from django.urls import path, include

from onlyfans.views import OnlyFansWorkpage, CreateNewTable, TableAPIView, TableDataAPIView

urlpatterns = [
    path('', OnlyFansWorkpage.as_view(), name='onlyfans_workpage'),
    path('create_table/', CreateNewTable.as_view(), name='onlyfans_new_table'),
    path('get_table_data/<int:table_id>/', OnlyFansWorkpage.get_data, name='get_table_data'),
    path('api/v1/table_test', TableAPIView.as_view(), name = 'test_api'),
    path('api/v1/data_test', TableDataAPIView.as_view(), name='data_api')
]