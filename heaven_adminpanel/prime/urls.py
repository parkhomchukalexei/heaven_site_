
from django.urls import path, include

from prime.views import PrimeWorkpage, CreateNewTable,TableDataSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'table_data', TableDataSet)


urlpatterns = [
    path('', PrimeWorkpage.as_view(), name='prime_workpage'),
    path('create_table/', CreateNewTable.as_view(), name='prime_new_table'),
    path('', include(router.urls)),

]