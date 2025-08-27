from rest_framework import serializers
from .models import PatchManagement
from hosts.models import Device


class PatchManagementSerializer(serializers.ModelSerializer):
    device_bios_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = PatchManagement
        fields = [
            "id", "title", "support", "kb",
            "mandatory", "reboot_required", "downloaded",
            "device", "device_bios_uuid", "download_patch", "install_patch"
        ]
        read_only_fields = ["device"]

    def create(self, validated_data):
        bios_uuid = validated_data.pop("device_bios_uuid")
        try:
            device = Device.objects.get(bios_uuid=bios_uuid)
        except Device.DoesNotExist:
            raise serializers.ValidationError({"device_bios_uuid": "Device not found"})

        validated_data["device"] = device
        return super().create(validated_data)
