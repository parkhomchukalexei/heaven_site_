
from django.urls import path, include
from onlyfans.views import  OnlyFansWorkpage, TableView
from rest_framework import routers
from onlyfans import views

router = routers.SimpleRouter()
router.register(r'table_data', views.TableDataSet)
router.register(r'table_view', views.TableView)


urlpatterns = [
    path('', OnlyFansWorkpage.as_view(), name='onlyfans_workpage'),
    # path('create_table/', CreateNewTable.as_view(), name='onlyfans_new_table'),
    path('', include(router.urls)),
]