
from django.urls import path, include

from prime.views import PrimeWorkpage, CreateNewTable,TableDataSet, TableViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'table_data', TableDataSet)
router.register(r'table', TableViewSet, basename='table')


urlpatterns = [
    path('', PrimeWorkpage.as_view(), name='prime_workpage'),
    path('create_table/', CreateNewTable.as_view(), name='prime_new_table'),
    path('', include(router.urls)),

]