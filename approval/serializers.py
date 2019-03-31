from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime
from rest_framework import serializers

from approval.models import SketchVote, SketchDecision, WallPhotoWrapperDecision
from workload.serializers import SketchSerializer, WallPhotoWrapperSerializer


class SketchVoteSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), required=False)

    class Meta:
        model = SketchVote
        fields = '__all__'


class SketchDecisionSerializer(serializers.ModelSerializer):
    sketch = SketchSerializer(read_only=True)
    owner_pk = serializers.IntegerField(write_only=True)
    group_role = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        # retrieve user
        try:
            user = get_user_model().objects.filter(pk=validated_data['owner_pk']).get()
        except KeyError:
            raise serializers.ValidationError('Cannot retrieve user pk in serializer')

        # check if user is in his responsive group
        for group in user.groups.all():
            if group == instance.group_role:
                break
        else:
            raise serializers.ValidationError('Permission denied: current user is not allowed to vote on this object')

        # check if vote is already filled
        if instance.vote is not None:
            raise serializers.ValidationError('Vote on this object is already done')

        # update object - vote
        try:
            instance.vote = validated_data['vote']
        except KeyError:
            raise serializers.ValidationError('Unable to retrieve vote in serializer')
        instance.owner = user
        instance.voted_at = datetime.now()

        instance.save()
        return instance

    class Meta:
        model = SketchDecision
        fields = '__all__'


class WallPhotoWrapperDecisionSerializer(serializers.ModelSerializer):
    wall_photo_wrapper = WallPhotoWrapperSerializer(read_only=True)
    owner_pk = serializers.IntegerField(write_only=True)
    group_role = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        # retrieve user
        try:
            user = get_user_model().objects.filter(pk=validated_data['owner_pk']).get()
        except KeyError:
            raise serializers.ValidationError('Cannot retrieve user pk in serializer')

        # check if user is in his responsive group
        for group in user.groups.all():
            if group == instance.group_role:
                break
        else:
            raise serializers.ValidationError('Permission denied: current user is not allowed to vote on this object')

        # check if vote is already filled
        if instance.vote is not None:
            raise serializers.ValidationError('Vote on this object is already done')

        # update object - vote
        try:
            instance.vote = validated_data['vote']
        except KeyError:
            raise serializers.ValidationError('Unable to retrieve vote in serializer')
        instance.owner = user
        instance.voted_at = datetime.now()

        instance.save()
        return instance

    class Meta:
        model = WallPhotoWrapperDecision
        fields = '__all__'
