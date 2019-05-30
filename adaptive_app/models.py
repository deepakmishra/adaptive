from django.db import models

class Config(models.Model):
	key = models.CharField(max_length = 128)
	value = models.CharField(max_length = 128)

class MCQQuestion(models.Model):
	text = models.CharField(max_length = 512)
	score = models.IntegerField()
	solvability = models.FloatField(default=0.0)
	initial_average_time = models.FloatField()

class MCQAnswer(models.Model):
	question = models.ForeignKey(MCQQuestion)
	text = models.CharField(max_length = 512)
	correct = models.BooleanField()

class User(models.Model):
	email = models.CharField(max_length = 256, unique = True)
	name = models.CharField(max_length = 256, unique = True)
	total_questions_attempted = models.IntegerField()
	last_score = models.IntegerField()
	last_test_taken = models.DateTimeField()

class UserAdaptiveTestLog(models.Model):
	choices = (('O', 'ONGOING'), ('P', 'PAUSED'), ('F','FINISHED'))
	user = models.ForeignKey(User)
	seconds_remaining = models.IntegerField()
	question_remaining_in_set = models.IntegerField()
	status = models.CharField(choices = choices, max_length = 1)

class Window(models.Model):
	test = models.ForeignKey(UserAdaptiveTestLog)
	window_start = models.IntegerField()
	window_end = models.IntegerField()

class UserAdaptiveTestAttemptLog(object):
	test = models.ForeignKey(UserAdaptiveTestLog)
	question = models.ForeignKey(MCQQuestion)
	answer = models.ForeignKey(MCQAnswer)
	unique_together = ('test', 'question')
