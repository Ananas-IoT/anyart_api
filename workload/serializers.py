from rest_framework import serializers

from workload.models import Document, Location, Workload, WallPhotoWrapper, WallPhoto


class WorkloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workload
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class WallPhotoWrapperSerializer(serializers.ModelSerializer):

    class Meta:
        model = WallPhotoWrapper
        fields = '__all__'


class WallPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = WallPhoto
        fields = '__all__'


class UserWallUploadSerializer(serializers.Serializer):
    workload = WorkloadSerializer()
    location = LocationSerializer()
    wall_photo_wrapper = WallPhotoWrapperSerializer()
    wall_photo = WallPhotoSerializer(many=True)

    def create(self, validated_data):
        ...


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('upload', )
