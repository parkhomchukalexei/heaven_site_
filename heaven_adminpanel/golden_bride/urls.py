
from django.urls import path, include

from golden_bride.views import GoldenBrideWorkpage, CreateNewTable, TableDataSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'table_data', TableDataSet)


urlpatterns = [
    path('', GoldenBrideWorkpage.as_view(), name='golden_bride_workpage'),
    path('create_table/', CreateNewTable.as_view(), name='golden_bride_new_table'),
    path('', include(router.urls)),
]