
from django.urls import path, include

from jump_for_love.views import JumpForLoveWorkpage, CreateNewTable, TableDataSet, TableViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'table_data', TableDataSet)
router.register(r'table', TableViewSet, basename='table')


urlpatterns = [
    path('', JumpForLoveWorkpage.as_view(), name='jump_for_love_workpage'),
    path('create_table/', CreateNewTable.as_view(), name='jump_for_love_new_table'),
    path('', include(router.urls)),

]