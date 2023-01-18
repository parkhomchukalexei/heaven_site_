
from django.urls import path, include

from anastasiadating.views import AnastasiaDatingWorkpage, CreateNewTable,TableDataSet, TableViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'table_data', TableDataSet)
router.register(r'table', TableViewSet, basename='table')


urlpatterns = [
    path('', AnastasiaDatingWorkpage.as_view(), name='anastasiadating_workpage'),
    path('create_table/', CreateNewTable.as_view(), name='anastasiadating_new_table'),
    path('', include(router.urls)),

]