from django.db import models
from datetime import datetime

class Config(models.Model):
	key = models.CharField(max_length = 128, unique = True)
	value = models.CharField(max_length = 128)

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
			if not Config.objects.filter(key = 'total_questions_attempted_to_be_eligigle').exists():
				Config(key='total_questions_attempted_to_be_eligigle', value=10).save()
			return self.total_questions_attempted >= int(Config.objects.get(key = 'total_questions_attempted_to_be_eligigle').value)
		else:
			test = self.useradaptivetestlog_set.order_by("-start_time")[0]
			return test.expiry_time <= datetime.now()

	@property
	def last_test(self):
		if not self.useradaptivetestlog_set.exists():
			return None
		return self.useradaptivetestlog_set.order_by("-start_time")[0]

class UserAdaptiveTestLog(models.Model):
	choices = (('O', 'ONGOING'), ('P', 'PAUSED'), ('F','FINISHED'))
	user = models.ForeignKey(UserProfile)
	seconds_remaining = models.IntegerField(default = 0)
	set_remaining = models.IntegerField(default = 0)
	question_remaining_in_set = models.IntegerField(default = 0)
	status = models.CharField(choices = choices, max_length = 1, default = 'F')
	start_time = models.DateTimeField(default=datetime.now, blank=True)
	window_start = models.IntegerField(default = 0)
	window_end = models.IntegerField(default = 0)

	@property
	def score(self):
		s = (self.window_start + self.window_end) / 2
		if s < 0:
			s = 0
		elif s > 100:
			s = 100
		return s

	@property
	def expiry_time(self):
		if not Config.objects.filter(key = 'test_expiry_time_in_days').exists():
			Config(key='test_expiry_time_in_days', value=60).save()
		return self.start_time + timedelta(days=int(Config.objects.get(key = 'test_expiry_time_in_days').value))

class UserAdaptiveTestAttemptLog(object):
	test = models.ForeignKey(UserAdaptiveTestLog)
	question = models.ForeignKey(MCQQuestion)
	answer = models.ForeignKey(MCQAnswer)
	seconds_time = models.IntegerField(default = 0)
	unique_together = ('test', 'question')
