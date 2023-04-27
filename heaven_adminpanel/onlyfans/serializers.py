from rest_framework import serializers
from .models import OnlyFansTable,TableData


class DataSerializer(serializers.ModelSerializer):

    def get_day(self, data_object):

        full_date = getattr(data_object, "date")
        return format(full_date, "%e").replace(" ","")

    day = serializers.SerializerMethodField('get_day')

    def __str__(self):
        return f'day_{self.day}'

    class Meta:
        model = TableData
        fields = ['id', 'day', 'data']




class TableSerializer(serializers.ModelSerializer):

    client_surname = serializers.PrimaryKeyRelatedField(read_only=True, source='client.surname')
    client_name = serializers.PrimaryKeyRelatedField(read_only=True, source='client.name')
    #operator_name = serializers.PrimaryKeyRelatedField(read_only=True, source= 'operator.username')
    #operator_surname = serializers.PrimaryKeyRelatedField(read_only=True, source= 'operator.last_name')
    tabledata_set = DataSerializer(many=True, read_only=True)

    class Meta:
        model = OnlyFansTable
        fields = ['client_name', 'client_surname','tabledata_set']

