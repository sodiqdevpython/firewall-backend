from rest_framework import serializers
from .models import Application, Connection


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class ConnectionSerializer(serializers.ModelSerializer):
    application_hash = serializers.CharField(write_only=True)

    class Meta:
        model = Connection
        fields = ['id', 'application_hash', 'protocol', 'local_address', 'remote_address', 'more_info']

    def create(self, validated_data):
        app_hash = validated_data.pop('application_hash')
        try:
            application = Application.objects.get(hash=app_hash)
        except Application.DoesNotExist:
            raise serializers.ValidationError({'application_hash': 'Invalid application hash'})
        connection = Connection.objects.create(application=application, **validated_data)
        return connection