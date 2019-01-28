from rest_framework import serializers

from workload.models import Location, Workload, WallPhotoWrapper, WallPhoto


class WallPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = WallPhoto
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class WorkloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workload
        fields = '__all__'


class WallPhotoWrapperSerializer(serializers.ModelSerializer):
    workload = WorkloadSerializer(many=False, required=True)
    location = LocationSerializer(many=False, required=True)
    wall_photos = WallPhotoSerializer(many=True, read_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = WallPhotoWrapper
        fields = '__all__'

    def create(self, validated_data):
        owner_id = int(validated_data.pop('user_id'))

        workload_data = validated_data.pop('workload')
        workload = Workload.objects.create(**workload_data)
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)
        wall_photos_data = self.context.get('view').request.FILES
        wall_photo_wrapper = WallPhotoWrapper.objects.create(**validated_data, owner_id=owner_id,
                                                             location=location, workload=workload)
        for wall_photo in wall_photos_data.values():
            WallPhoto.objects.create(photo=wall_photo, wrapper=wall_photo_wrapper)

        return wall_photo_wrapper
