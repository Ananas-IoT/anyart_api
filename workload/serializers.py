from django.contrib.auth.models import Group
from django.db import transaction, IntegrityError
from geopy import Nominatim
from rest_framework import serializers, exceptions
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from authorization.serializers import ReadOnlyUserSerializer
from approval.models import WallPhotoWrapperDecision, SketchDecision, SketchVote
from workload.models import Location, Workload, WallPhotoWrapper, WallPhoto, Sketch, SketchImage, Limitation

class OwnerSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()


class LocationSerializer(serializers.ModelSerializer):
    lng = serializers.FloatField(required=True, write_only=True)
    lat = serializers.FloatField(required=True, write_only=True)
    street_address = serializers.CharField(required=False, write_only=True, allow_blank=True)

    # self = NestedHyperlinkedRelatedField(
    #     read_only=True,
    #     source='*',
    #     view_name='location-limitations-detail',
    #     parent_lookup_kwargs={'wall_photo_wrapper_pk': 'photo_wrapper__pk',
    #                           'workload_pk': 'photo_wrapper__workload__pk',
    #                           'location_pk': 'limitation__location__pk'
    #                           }
    # )

    # limitations = serializers.SerializerMethodField()
    #
    # def get_limitations(self, instance):
    #     limitations = []
    #     for limitation_model in instance.limitations.all():
    #         limitations.append(limitation_model)
    #     return limitations

    class Meta:
        model = Location
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        geolocator = Nominatim()
        # location_id = int(validated_data.pop('location_id', None))
        lng = validated_data.pop('lng', None)
        lat = validated_data.pop('lat', None)
        street_address = validated_data.pop('street_address', None)
        #owner_id = int(validated_data.pop('user_id', None))

        if lat > 0:
            location = geolocator.reverse("{}, {}".format(lng, lat))
            street_address = location.address
            street_address = street_address.split(', ')[0] + ", " + street_address.split(', ')[1]
            print(street_address)
        else:
            location = geolocator.geocode(street_address)
            lat = location.latitude
            lng = location.longitude

        data = {'lat': lat, 'lng': lng, 'street_address': street_address}
        location = Location.objects.create(**data)

        # limitations_serializer = LimitationSerializer(data={'authority_id':10,'reason':'smth','location_id':location._get_pk_val()}, many=True)
        # print(limitations_serializer.initial_data)
        #
        # if limitations_serializer.is_valid():
        #
        #     print(1)
        #     limitations = limitations_serializer.save()
        #     print(limitations)
        # else:
        #     print(limitations_serializer.errors)
        #     #limitations_data = self.context.get('view').request.FILES
        # print(limitations.__dir__)
        return location


    def update(self, instance, validated_data):
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lng = validated_data.get('lng', instance.lng)
        instance.street_address = validated_data.get('street_address', instance.street_address)
        return instance


class WorkloadSerializer(serializers.Serializer):
    lng = serializers.FloatField(required=True, write_only=True)
    lat = serializers.FloatField(required=True, write_only=True)

    street_address = serializers.CharField(required=False, write_only=True, allow_blank=True)

    description = serializers.CharField(required=True, write_only=True)
    user_id = serializers.CharField(write_only=True, required=False)
    images = serializers.ListField(child=serializers.ImageField(
        allow_empty_file=False,
        use_url=False
    ), required=True, write_only=True)

    self = serializers.HyperlinkedIdentityField(view_name='workload-detail')
    wall_photo_wrapper = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='workload-wall_photo_wrapper-detail',
        parent_lookup_kwargs={'workload_pk': 'workload__pk'}
    )

    def create(self, validated_data):
        # Data retrieval
        owner_id = int(validated_data.pop('user_id', None))
        print(owner_id)
        lng = validated_data.pop('lng', None)
        lat = validated_data.pop('lat', None)

        street_address = validated_data.pop('street_address', None)

        description = validated_data.pop('description', None)

        # Object creation
        workload = Workload.objects.create()

        location_serializer = LocationSerializer(data={'lat': lat, 'lng': lng, 'street_address': street_address, 'user_id':owner_id})

        if location_serializer.is_valid():
            location = location_serializer.save()

        wall_photo_wrapper = WallPhotoWrapper.objects.create(description=description, owner_id=owner_id,
                                                             location=location, workload=workload)

        # decisions
        groups = Group.objects.all()

        # Saving & wall photo uploading
        try:
            with transaction.atomic():
                location.save()
                workload.save()
                wall_photo_wrapper.save()
                for wall_photo in list(validated_data.pop('images')):
                    wall_photo = WallPhoto.objects.create(photo=wall_photo, wrapper=wall_photo_wrapper)
                    wall_photo.save()

                # creating decisions
                for group in groups:
                    decision = WallPhotoWrapperDecision.objects.create(group_role=group,
                                                                       wall_photo_wrapper=wall_photo_wrapper)
                    decision.save()

        except IntegrityError:
            return exceptions.ValidationError('error on Workload serializer')

        return workload

    def update(self, instance, validated_data):
        # Data update
        instance.requirements = validated_data.pop('requirements', instance.workload.requirements)
        instance.location.lng = validated_data('lng', instance.location.lng)
        instance.location.lat = validated_data('lat', instance.location.lat)
        instance.location.street_address = validated_data('street_address', instance.location.street_address)
        instance.description = validated_data.pop('description', instance.description)

        # Files
        wall_photos_data = self.context.get('view').request.FILES
        for wall_photo in wall_photos_data.values():
            WallPhoto.objects.create(photo=wall_photo, wrapper=instance)

        # Saving
        instance.save()

        return instance


class ReadOnlyWorkloadSerializer(serializers.ModelSerializer):
    wall_photo_wrapper = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='workload-wall_photo_wrapper-detail',
        parent_lookup_kwargs={'workload_pk': 'workload__pk'}
    )

    class Meta:
        model = Workload
        fields = '__all__'


class WallPhotoWrapperLocationSerializer(serializers.Serializer):
    lng = serializers.FloatField()
    lat = serializers.FloatField()
    street_address = serializers.CharField()
    self = NestedHyperlinkedRelatedField(
        read_only=True,
        source='*',
        view_name='wrapper-location-detail',
        parent_lookup_kwargs={'wall_photo_wrapper_pk': 'photo_wrapper__pk',
                              'workload_pk': 'photo_wrapper__workload__pk'}
    )

    def update(self, instance, validated_data):
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lng = validated_data.get('lng', instance.lng)
        instance.street_address = validated_data.get('street_address', instance.street_address)
        return instance


class WallPhotoWrapperSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True)
    workload_id = serializers.PrimaryKeyRelatedField(queryset=Workload.objects.all(), source='Workload', required=False)
    created_at = serializers.DateTimeField(read_only=True)
    owner = OwnerSerializer(read_only=True)

    # location
    lng = serializers.FloatField(required=True, write_only=True)
    lat = serializers.FloatField(required=True, write_only=True)
    street_address = serializers.CharField(required=False, write_only=True)

    location = WallPhotoWrapperLocationSerializer(read_only=True)
    workload = serializers.HyperlinkedRelatedField(view_name='workload-detail', read_only=True)
    wall_photos = serializers.SerializerMethodField()
    sketch_count = serializers.SerializerMethodField()

    def get_wall_photos(self, instance):
        wall_photos = []
        for wall_photo_model in instance.wall_photos.all():
            wall_photos.append(wall_photo_model.photo.url)
        return wall_photos

    def get_sketch_count(self, obj):
        return obj.workload.sketch_set.count()

    class Meta:
        model = WallPhotoWrapper
        fields = '__all__'


    def create(self, validated_data):
        # Data retrieval
        owner_id = int(validated_data.pop('user_id'))
        lng = validated_data.pop('lng')
        lat = validated_data.pop('lat')
        street_address = validated_data.pop('street_address')
        description = validated_data.pop('description')
        workload_id = validated_data.pop('workload_id')

        # Object creation

        location_serializer = LocationSerializer(**validated_data)
        if location_serializer.is_valid():
            location = location_serializer.save()


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
    workload = serializers.PrimaryKeyRelatedField(queryset=Workload.objects.all(),
                                                  source='workload.Workload', required=False)
    owner = OwnerSerializer(read_only=True)
    workload_id = serializers.IntegerField(write_only=True, required=False)
    user_id = serializers.CharField(write_only=True, required=False)
    sketch_images = serializers.SerializerMethodField()
    sketch_votes = serializers.SerializerMethodField(read_only=True)
    vote_id = serializers.SerializerMethodField(read_only=True)
    images = serializers.ListField(child=serializers.ImageField(
        allow_empty_file=False,
        use_url=False
    ), required=True, write_only=True)

    def get_vote_id(self, obj):
        try:
            return obj.sketch_votes.filter(owner_id=self.context.get('request').user.id, sketch_id=obj.id, vote=1) \
                .get().id
        except SketchVote.DoesNotExist:
            return 0

    def get_sketch_votes(self, obj):
        return obj.sketch_votes.filter(vote=1).count()

    def get_sketch_images(self, instance):
        images = []
        for image_model in instance.sketch_images.all():
            images.append(image_model.image.url)
        return images

    class Meta:
        model = Sketch
        fields = '__all__'

    def create(self, validated_data):
        # Data retrieval
        owner_id = int(validated_data.pop('user_id'))
        images = validated_data.pop('images')

        # Object creation
        sketch = Sketch.objects.create(**validated_data, owner_id=owner_id)

        # decisions
        groups = Group.objects.all()

        # Saving & creating sketch images
        try:
            with transaction.atomic():
                sketch.save()
                for image in images:
                    sketch_image = SketchImage.objects.create(image=image, sketch=sketch)
                    sketch_image.save()

                # creating decisions
                for group in groups:
                    decision = SketchDecision.objects.create(group_role=group,
                                                             sketch=sketch)
                    decision.save()
        except IntegrityError:
            return exceptions.ValidationError

        return sketch

    def update(self, instance, validated_data):
        sketch_files_data = self.context.get('view').request.FILES
        instance.workload = validated_data.pop('workload', instance.workload)
        instance.sketch_description = validated_data.pop('sketch_description', instance.sketch_description)

        for image in sketch_files_data.values():
            SketchImage.objects.create(image=image, sketch=instance)

        instance.save()

        return instance


class WallPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(read_only=True, required=False)
    wrapper = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = WallPhoto
        fields = '__all__'

    def create(self, validated_data):
        photo = next(self.context.get('view').request.FILES.values())
        wrapper_pk = validated_data.pop('wrapper', None)

        wall_photo = WallPhoto.objects.create(photo=photo, wrapper_id=wrapper_pk)
        wall_photo.save()

        return wall_photo

    def update(self, instance, validated_data):
        photo = next(self.context.get('view').request.FILES.values())

        instance.photo = photo or instance.photo
        instance.save()

        return instance


class SketchImageSerializer(serializers.ModelSerializer):
    sketch = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='workload-sketch-detail',
        parent_lookup_kwargs={
            'workload_pk': 'workload__pk'
        }
    )
    sketch_pk = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        image = next(self.context.get('view').request.FILES.values())
        sketch_id = validated_data.pop('sketch_pk', None)

        sketch = SketchImage.objects.create(image=image, sketch_id=sketch_id)
        sketch.save()
        return sketch

    def update(self, instance, validated_data):
        image = next(self.context.get('view').request.FILES.values())

        instance.image = image or instance.image
        instance.save()

        return instance

    class Meta:
        model = SketchImage
        fields = '__all__'


class LimitationSerializer(serializers.Serializer):
    authority_id = serializers.IntegerField(required=True, write_only=True)
    location_id = serializers.IntegerField(required=True, write_only=True)
    reason = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Location
        fields = '__all__'

    def create(self, validated_data):
        authority_id = int(validated_data.pop('authority_id', None))
        location_id = int(validated_data.pop('location_id', None))
        reason = validated_data.pop('reason', None)
        print(1)
        limitation = Limitation.objects.create(authority_id=authority_id, reason=reason, location_id=location_id)
        #limitation = Limitation.objects.create(**validated_data)
        limitation.save()
        return limitation

    def update(self, instance, validated_data):
        instance.authority = validated_data.get('autority', instance.authority)
        instance.reason = validated_data.get('reason', instance.reason)
        return instance
