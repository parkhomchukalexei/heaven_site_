
from django.urls import path, include

from romans_compass.views import RomansCompassWorkpage, CreateNewTable, TableDataSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'table_data', TableDataSet)


urlpatterns = [
    path('', RomansCompassWorkpage.as_view(), name='romans_compass_workpage'),
    path('create_table/', CreateNewTable.as_view(), name='romans_compass_new_table'),
    path('', include(router.urls)),

]