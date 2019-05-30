from problems.models import MCQQuestion, MCQAnswer, UserProfile, UserAdaptiveTestLog
from rest_framework import serializers

class UserAdaptiveTestLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserAdaptiveTestLog
        fields = ('score', 'expiry_time', 'status',)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    last_test = UserAdaptiveTestLogSerializer(many=False)

    class Meta:
        model = UserProfile
        fields = ('name', 'email', 'eligible', 'last_test',)