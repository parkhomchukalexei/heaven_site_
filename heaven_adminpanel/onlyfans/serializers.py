from rest_framework import serializers


class TableSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    date = serializers.DateField()
    table_type = serializers.BooleanField()
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    operator = serializers.PrimaryKeyRelatedField(read_only=True)


class DataSerializer(serializers.Serializer):
    date = serializers.DateField()
    data = serializers.FloatField()
    data_type = serializers.CharField(max_length=255)
    table_id = serializers.IntegerField()
