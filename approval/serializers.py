from django.contrib.auth import get_user_model
from rest_framework import serializers

from approval.models import SketchVote


class SketchVoteSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), required=False)

    class Meta:
        model = SketchVote
        fields = '__all__'
