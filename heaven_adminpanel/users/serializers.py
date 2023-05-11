from rest_framework import serializers
from users.models import Client, User


class ClientSerializer(serializers.ModelSerializer):
    def get_full_name(self, object):
        name = getattr(object, 'name')
        surname = getattr(object, 'surname')
        print(name)
        print(surname)
        return f'{name} {surname}'

    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = Client
        fields = ["full_name"]



class PermissionSerializer(serializers.ModelSerializer):

    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "first_name", 'user_permissions')

    def get_user_permissions(self, obj):
        return list(obj._user_get_permissions("all"))

