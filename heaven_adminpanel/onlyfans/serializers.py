from rest_framework import serializers
from .models import OnlyFansTable,TableData


class DataSerializer(serializers.ModelSerializer):

    def get_day(self,data_object):
        full_date = getattr(data_object, "date")
        return format(full_date, "%e").replace(" ","")

    day = serializers.SerializerMethodField('get_day')
    class Meta:
        model = TableData
        fields = "__all__"






class TableSerializer(serializers.ModelSerializer):

    #table_information = DataSerializer(many=True, read_only=True)
    client_surname = serializers.PrimaryKeyRelatedField(read_only=True, source= "client.surname")
    client_name = serializers.PrimaryKeyRelatedField(read_only=True, source= "client.name")
    operator_name = serializers.PrimaryKeyRelatedField(read_only=True, source= 'operator.username')
    operator_surname = serializers.PrimaryKeyRelatedField(read_only=True, source= 'operator.last_name')

    class Meta:
        model = OnlyFansTable
        fields = '__all__'






