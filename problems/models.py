from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class Config(models.Model):
	key = models.CharField(max_length = 128, unique = True)
	value = models.CharField(max_length = 128)

	@staticmethod
	def get(key, default_value):
		if not Config.objects.filter(key = key).exists():
			Config(key=key, value=default_value).save()
		return Config.objects.get(key = key).value
 
class MCQQuestion(models.Model):
	text = models.TextField()
	score = models.IntegerField()
	solvability = models.FloatField(default=0.0)
	initial_average_time = models.FloatField()

class MCQAnswer(models.Model):
	question = models.ForeignKey(MCQQuestion)
	text = models.TextField()
	correct = models.BooleanField()

class UserProfile(models.Model):
	email = models.CharField(max_length = 255, unique = True)
	name = models.CharField(max_length = 255)
	total_questions_attempted = models.IntegerField(default = 0)

	@property
	def eligible(self):
		if not self.useradaptivetestlog_set.exists():
			return self.total_questions_attempted >= int(Config.get('total_questions_attempted_to_be_eligigle', 10))
		else:
			test = self.useradaptivetestlog_set.order_by("-start_time")[0]
			return test.status in ['O', 'P'] or test.expiry_time <= timezone.now()

	@property
	def last_test(self):
		if not self.useradaptivetestlog_set.exists():
			return None
		return self.useradaptivetestlog_set.order_by("-start_time")[0]

class UserAdaptiveTestLog(models.Model):
	choices = (('O', 'ONGOING'), ('P', 'PAUSED'), ('F','FINISHED'))
	user = models.ForeignKey(UserProfile)
	set_remaining = models.IntegerField(default = 0)
	question_remaining_in_set = models.IntegerField(default = 0)
	status = models.CharField(choices = choices, max_length = 1, default = 'O')
	start_time = models.DateTimeField(default=timezone.now)
	window_start = models.IntegerField(default = 0)
	window_end = models.IntegerField(default = 0)

	@property
	def score(self):
		s = (self.window_start + self.window_end) / 2
		if s < 0:
			s = 0
		elif s > 100:
			s = 100
		return round(s)

	@property
	def expiry_time(self):
		return self.start_time + timedelta(days=int(Config.get('test_expiry_time_in_days', 60)))


class UserAdaptiveTestScoreLog(models.Model):
	test = models.ForeignKey(UserAdaptiveTestLog)
	set_number = models.IntegerField(default = 0)
	score = models.IntegerField(default = 0)
	unique_together = ('test', 'set_number')


class UserAdaptiveTestAttemptLog(models.Model):
	choices = (('W', 'WAITING'), ('F','FINISHED'))
	test = models.ForeignKey(UserAdaptiveTestLog)
	question = models.ForeignKey(MCQQuestion)
	answer = models.ForeignKey(MCQAnswer, null=True)
	start_time = models.DateTimeField(default=timezone.now)
	end_time = AutoDateTimeField(default=timezone.now)
	status = models.CharField(choices = choices, max_length = 1, default = 'W')
	unique_together = ('test', 'question')
