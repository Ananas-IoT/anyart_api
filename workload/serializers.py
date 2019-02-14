from rest_framework import serializers

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


class WorkloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workload
        # fields = '__all__'
        # todo list fields explicitly
        exclude = ('status', 'requirements')


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

    def update(self, instance, validated_data):

        workload_data = validated_data.pop('workload', None)
        if workload_data:
            instance.workload.requirements = workload_data.pop('requirements', instance.workload.requirements)
        location_data = validated_data.pop('location', None)
        if location_data:
            instance.location.lng = location_data.pop('lng', instance.location.lng)
            instance.location.lat = location_data.pop('lat', instance.location.lat)
        wall_photos_data = self.context.get('view').request.FILES
        for wall_photo in wall_photos_data.values():
            WallPhoto.objects.create(photo=wall_photo, wrapper=instance)

        instance.description = validated_data.pop('description', instance.description)
        instance.save()

        return instance


class SketchSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)
    sketches = SketchImageSerializer(many=True, read_only=True)

    class Meta:
        model = Sketch
        fields = '__all__'

    def create(self, validated_data):
        owner_id = int(validated_data.pop('user_id'))

        sketch = Sketch.objects.create(**validated_data, owner_id=owner_id)
        sketch_files_data = self.context.get('view').request.FILES

        for image in sketch_files_data.values():
            SketchImage.objects.create(image=image, sketch=sketch)

        return sketch

    def update(self, instance, validated_data):
        sketch_files_data = self.context.get('view').request.FILES
        instance.workload = validated_data.pop('workload', instance.workload)

        for image in sketch_files_data.values():
            SketchImage.objects.create(image=image, sketch=instance)

        instance.save()

        return instance