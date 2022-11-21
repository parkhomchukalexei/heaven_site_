
from django.urls import path, include
from rest_framework import routers
from users.views import Register, CreateClient, ClientList, ClientPage, DeleteClient, ClientAPI

router = routers.DefaultRouter()
router.register(r'client_api', ClientAPI, basename='client')


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('create_client/', CreateClient.as_view(), name='create_client'),
    path('client_list/', ClientList.as_view(), name='client_list'),
    path('client/<int:client_id>', ClientPage.as_view(), name='client_page'),
    path('delete_client/<int:client_id>', DeleteClient.as_view(), name='delete_client'),
    path('', include(router.urls))
]
