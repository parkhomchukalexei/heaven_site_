
from django.urls import path, include
from onlyfans.views import OnlyFansWorkpage, CreateNewTable,TableViewSet
from rest_framework import routers
from onlyfans import views

router = routers.DefaultRouter()
router.register(r'table_data', views.TableDataSet)
#router.register(r'table', views.TableViewSet, basename='table')


urlpatterns = [
    path('', OnlyFansWorkpage.as_view(), name='onlyfans_workpage'),
    path('create_table/', CreateNewTable.as_view(), name='onlyfans_new_table'),
    path('', include(router.urls)),
    path('api/', TableViewSet.as_view({'get':{'hui'}}), name='table_set')

]