from problems.models import MCQQuestion, MCQAnswer, UserProfile, UserAdaptiveTestLog, UserAdaptiveTestScoreLog
from rest_framework import serializers

class UserAdaptiveTestScoreLogSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = UserAdaptiveTestScoreLog
		fields = ('set_number', 'score',)

class UserAdaptiveTestLogSerializer(serializers.HyperlinkedModelSerializer):

	analytics = UserAdaptiveTestScoreLogSerializer(many=True, source='useradaptivetestscorelog_set') 

	class Meta:
		model = UserAdaptiveTestLog
		fields = ('score', 'expiry_time', 'status', 'analytics',)

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
