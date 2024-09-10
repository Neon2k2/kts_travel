from rest_framework import serializers

class LogSerializer(serializers.Serializer):
    driver = serializers.CharField(max_length=100)
    car = serializers.CharField(max_length=100)
    date = serializers.DateTimeField()
    properties = serializers.JSONField()
    status = serializers.CharField(required=False)