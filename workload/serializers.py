from django.db import transaction, IntegrityError
from rest_framework import serializers, exceptions
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from workload.models import Location, Workload, WallPhotoWrapper, WallPhoto, Sketch, SketchImage


class SketchImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SketchImage
        fields = '__all__'


class WallPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(read_only=True, required=False)

    class Meta:
        model = WallPhoto
        fields = '__all__'



    def create(self, validated_data):
        photo = next(self.context.get('view').request.FILES.values())
        wrapper = validated_data.pop('wrapper', None)

        wall_photo = WallPhoto.objects.create(photo=photo, wrapper=wrapper)
        wall_photo.save()

        return wall_photo

    def update(self, instance, validated_data):
        photo = next(self.context.get('view').request.FILES.values())

        instance.photo = photo or instance.photo
        instance.save()

        return instance


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class WorkloadSerializer(serializers.Serializer):
    lng = serializers.FloatField(required=True, write_only=True)
    lat = serializers.FloatField(required=True, write_only=True)
    requirements = serializers.CharField(required=True, write_only=True)
    description = serializers.CharField(required=True, write_only=True)
    user_id = serializers.CharField(write_only=True)

    self = serializers.HyperlinkedIdentityField(view_name='workload-detail')
    wall_photo_wrappers = serializers.HyperlinkedRelatedField(many=True, view_name='wall_photo_wrapper-detail',
                                                              read_only=True)

    def create(self, validated_data):
        # Data retrieval
        owner_id = int(validated_data.pop('user_id'))
        lng = validated_data.pop('lng')
        lat = validated_data.pop('lat')
        requirements = validated_data.pop('requirements')
        description = validated_data.pop('description')

        # Object creation
        workload = Workload.objects.create(requirements=requirements)
        location = Location.objects.create(lng=lng, lat=lat)

        # Files
        wall_photos_data = self.context.get('view').request.FILES
        wall_photo_wrapper = WallPhotoWrapper.objects.create(description=description, owner_id=owner_id,
                                                             location=location, workload=workload)

        # Saving & wall photo uploading
        try:
            with transaction.atomic():
                location.save()
                workload.save()
                wall_photo_wrapper.save()
                for wall_photo in wall_photos_data.values():
                    wall_photo = WallPhoto.objects.create(photo=wall_photo, wrapper=wall_photo_wrapper)
                    wall_photo.save()
        except IntegrityError:
            return exceptions.ValidationError

        return workload

    def update(self, instance, validated_data):
        # Data update
        instance.workload.requirements = validated_data.pop('requirements', instance.workload.requirements)
        instance.location.lng = validated_data('lng', instance.location.lng)
        instance.location.lat = validated_data('lat', instance.location.lat)
        instance.description = validated_data.pop('description', instance.description)

        # Files
        wall_photos_data = self.context.get('view').request.FILES
        for wall_photo in wall_photos_data.values():
            WallPhoto.objects.create(photo=wall_photo, wrapper=instance)

        # Saving
        instance.save()

        return instance


class WallPhotoWrapperSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)
    workload_id = serializers.IntegerField(write_only=True)
    lng = serializers.FloatField(required=True, write_only=True)
    lat = serializers.FloatField(required=True, write_only=True)
    location = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='wrapper-location-detail',
        parent_lookup_kwargs={'wall_photo_wrapper_pk': 'photo_wrapper__pk',
                              'workload_pk': 'photo_wrapper__workload__pk'}
    )
    workload = serializers.HyperlinkedRelatedField(view_name='workload-detail', read_only=True)
    wall_photos = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='wrapper-wall_photo-detail',
        parent_lookup_kwargs={'wall_photo_wrapper_pk': 'wrapper__pk',
                              'workload_pk': 'wrapper__workload__pk'}
    )

    class Meta:
        model = WallPhotoWrapper
        fields = '__all__'

    def create(self, validated_data):
        # Data retrieval
        owner_id = int(validated_data.pop('user_id'))
        lng = validated_data.pop('lng')
        lat = validated_data.pop('lat')
        description = validated_data.pop('description')
        workload_id = validated_data.pop('workload_id')

        # Object creation
        location = Location.objects.create(lng=lng, lat=lat)

        # Files
        wall_photos_data = self.context.get('view').request.FILES
        wall_photo_wrapper = WallPhotoWrapper.objects.create(description=description, owner_id=owner_id,
                                                             location=location, workload_id=workload_id)

        # Saving & wall photo uploading
        try:
            with transaction.atomic():
                location.save()
                wall_photo_wrapper.save()
                for wall_photo in wall_photos_data.values():
                    wall_photo = WallPhoto.objects.create(photo=wall_photo, wrapper=wall_photo_wrapper)
                    wall_photo.save()
        except IntegrityError:
            return exceptions.ValidationError

        return wall_photo_wrapper


class SketchSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)
    sketch_images = SketchImageSerializer(many=True, read_only=True)

    class Meta:
        model = Sketch
        fields = '__all__'

    def create(self, validated_data):
        # Data retrieval
        owner_id = int(validated_data.pop('user_id'))

        # Object creation
        sketch = Sketch.objects.create(**validated_data, owner_id=owner_id)

        # Files
        sketch_files_data = self.context.get('view').request.FILES

        # Saving & creating sketch images
        try:
            with transaction.atomic():
                sketch.save()
                for image in sketch_files_data.values():
                    sketch_image = SketchImage.objects.create(image=image, sketch=sketch)
                    sketch_image.save()
        except IntegrityError:
            return exceptions.ValidationError

        return sketch

    def update(self, instance, validated_data):
        sketch_files_data = self.context.get('view').request.FILES
        instance.workload = validated_data.pop('workload', instance.workload)

        for image in sketch_files_data.values():
            SketchImage.objects.create(image=image, sketch=instance)

        instance.save()

        return instance


class ReadOnlyWorkloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workload
        fields = '__all__'