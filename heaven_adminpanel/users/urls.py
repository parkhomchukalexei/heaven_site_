
from django.urls import path, include

from users.views import Register, CreateClient, ClientList, ClientPage, DeleteClient

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('create_client/', CreateClient.as_view(), name='create_client'),
    path('client_list/', ClientList.as_view(), name='client_list'),
    path('client/<str:name>', ClientPage.as_view(), name='client_page'),
    path('delete_client/<int:client_id>', DeleteClient.as_view(), name='delete_client'),
]
