from rest_framework import serializers
from .models import OnlyFansTable,TableData


class DataSerializer(serializers.ModelSerializer):

    def get_day(self, data_object):

        full_date = getattr(data_object, "date")
        return format(full_date, "%e").replace(" ","")

    def sum(self, data_object):
        total_sum =+ float(getattr(data_object,'data'))
        return total_sum

    day = serializers.SerializerMethodField('get_day')
    totalSum = serializers.SerializerMethodField('sum')

    def __str__(self):
        return f'day_{self.day}'

    class Meta:
        model = TableData
        fields = '__all__'




class TableSerializer(serializers.ModelSerializer):

    clientSurname = serializers.PrimaryKeyRelatedField(read_only=True, source='client.surname')
    clientName = serializers.PrimaryKeyRelatedField(read_only=True, source='client.name')
    #operator_name = serializers.PrimaryKeyRelatedField(read_only=True, source= 'operator.username')
    #operator_surname = serializers.PrimaryKeyRelatedField(read_only=True, source= 'operator.last_name')
    tabledata_set = DataSerializer(many=True, read_only=True)


    class Meta:
        model = OnlyFansTable
        fields = '__all__'


class UserAndClientSerializer(serializers.Serializer):


    client = serializers.SerializerMethodField('getClientNameSurname')
    operator = serializers.SerializerMethodField('getOperatorNameSurname')
    def getClientNameSurname(self, data_object):

        name = getattr(data_object,'name')
        surname = getattr(data_object, 'surname')
        return f"{name} {surname}"

    def getOperatorNameSurname(self,data_object):
        name = getattr(data_object, 'name')
        surname = getattr(data_object, 'surname')
        return f"{name}, {surname}"


class TableCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnlyFansTable
        fields = '__all__'
