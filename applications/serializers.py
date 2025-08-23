from rest_framework import serializers
from .models import Application, Connection
from hosts.models import Device


class ApplicationSerializer(serializers.ModelSerializer):
    host = serializers.CharField(write_only=True)
    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        bios_uuid = validated_data.pop('host')
        try:
            device = Device.objects.get(bios_uuid=bios_uuid)
            print(device)
        except Device.DoesNotExist:
            raise serializers.ValidationError(
                {"bios_uuid": "Device not found."})

        validated_data['host'] = device
        return super().create(validated_data)


class ConnectionSerializer(serializers.ModelSerializer):
    application_hash = serializers.CharField(write_only=True)

    class Meta:
        model = Connection
        fields = ['id', 'application_hash',
                  'local_address', 'remote_address', 'more_info']

    def create(self, validated_data):
        app_hash = validated_data.pop('application_hash')
        try:
            application = Application.objects.filter(hash=app_hash).first()
        except Application.DoesNotExist:
            raise serializers.ValidationError(
                {'application_hash': 'Invalid application hash'})
        connection = Connection.objects.create(
            application=application, **validated_data)
        return connection
