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
		fields = ('id', 'name', 'email', 'eligible', 'last_test',)


class MCQAnswerSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = MCQAnswer
		fields = ('id', 'text', 'correct',)	


class MCQQuestionSerializer(serializers.HyperlinkedModelSerializer):

	answers = MCQAnswerSerializer(many=True, source='mcqanswer_set') 

	class Meta:
		model = MCQQuestion
		fields = ('id', 'text', 'answers')

