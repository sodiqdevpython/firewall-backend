from rest_framework import serializers
from .models import Application, Connection
from hosts.models import Device


class ConnectionBulkCreateSerializer(serializers.ModelSerializer):
    local = serializers.CharField(write_only=True)
    remote = serializers.CharField(write_only=True)

    class Meta:
        model = Connection
        exclude = ["application", "local_address", "remote_address"]

    def validate(self, attrs):
        local_ip, local_port = attrs["local"].split(":")
        remote_ip, remote_port = attrs["remote"].split(":")

        attrs["local_address"] = local_ip
        attrs["remote_address"] = remote_ip

        return attrs


class ApplicationSerializer(serializers.ModelSerializer):
    host = serializers.CharField()
    ip_address = serializers.CharField(source="host.ip_address", read_only=True)
    connections = ConnectionBulkCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        connections_data = validated_data.pop("connections", [])
        bios_uuid = validated_data.pop("host")

        try:
            device = Device.objects.get(bios_uuid=bios_uuid)
        except Device.DoesNotExist:
            raise serializers.ValidationError({"host": f"Device {bios_uuid} not found"})
        validated_data["host"] = device

        application = super().create(validated_data)

        connection_objs = []
        for conn in connections_data:
            local_ip = conn["local"].split(":")[0]
            remote_ip = conn["remote"].split(":")[0]

            connection_objs.append(Connection(
                application=application,
                timestamp=conn["timestamp"],
                direction=conn["direction"],
                local_address=local_ip,
                remote_address=remote_ip,
                bytes=conn["bytes"],
            ))
        if connection_objs:
            Connection.objects.bulk_create(connection_objs)

        return application


class ConnectionSerializer(serializers.ModelSerializer):
    hash = serializers.CharField(write_only=True)
    application = ApplicationSerializer(read_only=True)

    class Meta:
        model = Connection
        fields = ['id', 'hash', "application",
                  'local_address', 'remote_address', 'more_info', "direction"]

    def create(self, validated_data):
        app_hash = validated_data.pop('hash')
        try:
            application = Application.objects.filter(hash=app_hash).first()
        except Application.DoesNotExist:
            raise serializers.ValidationError(
                {'hash': 'Invalid application hash'})
        connection = Connection.objects.create(
            application=application, **validated_data)
        return connection
