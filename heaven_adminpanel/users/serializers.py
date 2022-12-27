from django.contrib.auth.models import Permission
from rest_framework import serializers
from users.models import Client, User


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'



class PermissionSerializer(serializers.ModelSerializer):

    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "first_name", 'user_permissions')

    def get_user_permissions(self, obj):
        return list(obj._user_get_permissions("all"))