
from django.urls import path, include

from charm_date.views import CharmDateWorkpage, CreateNewTable, TableDataSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'table_data', TableDataSet)


urlpatterns = [
    path('', CharmDateWorkpage.as_view(), name='charm_date_workpage'),
    path('create_table/', CreateNewTable.as_view(), name='charm_date_new_table'),
    path('', include(router.urls)),

]