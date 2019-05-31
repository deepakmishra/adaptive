from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from problems.models import MCQQuestion, MCQAnswer, UserProfile, UserAdaptiveTestLog, UserAdaptiveTestAttemptLog, Config, UserAdaptiveTestScoreLog
from problems.serializers import UserProfileSerializer, MCQQuestionSerializer, UserAdaptiveTestScoreLogSerializer
from django.http import JsonResponse, HttpResponse
from datetime import timedelta
from django.utils import timezone
from django.db.models import F
import random, json, math


def test_page(request):
	return render(request, "index.html")

@csrf_exempt
def email_profile(request):
	email = request.POST.get('email')
	if not UserProfile.objects.filter(email=email).exists():
		return JsonResponse({})

	user = UserProfile.objects.get(email=email)
	user_json = UserProfileSerializer(user).data
	return JsonResponse(user_json)

@csrf_exempt
def user_profile(request, id):
	user = UserProfile.objects.get(id=id)
	user_json = UserProfileSerializer(user).data
	return JsonResponse(user_json)

@csrf_exempt
def start_test(request, id):
	user = UserProfile.objects.get(id=id)
	if not user.eligible:
		return HttpResponse(status=412, reason="Not Eligible")

	status = 'O'

	started_time = timezone.now() - timedelta(seconds=int(Config.get('test_total_time_in_seconds', 3600)))

	if UserAdaptiveTestLog.objects.filter(user = user, status = status, start_time__gt = started_time).exists():
		test = UserAdaptiveTestLog.objects.filter(user = user, status = status, start_time__gt = started_time).order_by('-start_time')[0]
		if test:
			UserAdaptiveTestLog.objects.filter(user = user).exclude(id=test.id).update(status = 'F')
	else:
		set_remaining = int(Config.get('test_number_of_sets', 10))
		question_remaining_in_set = int(Config.get('number_of_questions_in_sets', 5))
		window_start = int(Config.get('window_initial_value', 45))
		window_size = int(Config.get('window_size', 10))
		window_end = window_start + window_size
		test = UserAdaptiveTestLog(user = user, set_remaining = set_remaining, question_remaining_in_set = question_remaining_in_set, 
			window_start = window_start, window_end = window_end, status = status)
		test.save()
		UserAdaptiveTestScoreLog(test=test, set_number=0, score=test.score).save()

	next_question = get_next_question(test)
	UserAdaptiveTestAttemptLog(test = test, question = next_question).save()
	question_json = MCQQuestionSerializer(next_question).data

	remaining_time = test.start_time - timezone.now() + timedelta(seconds=int(Config.get('test_total_time_in_seconds', 3600)))
	question_json['remaining_time_in_seconds'] = remaining_time.total_seconds()
	question_json['question_number'] = test.useradaptivetestattemptlog_set.count()
	#if test.score > int(Config.get('minimum_score_to_display_score', 80)):
	question_json['test_score'] = test.score

	return JsonResponse(question_json)

@csrf_exempt
def attempt_question(request, id):
	if request.method == 'GET':
		answer_id = int(request.GET.get('answer_id'))
		#return HttpResponse(status=405)
	elif request.method == 'POST':
		answer_id = int(request.POST.get('answer_id'))
	else:
		print "returned here 0"
		return HttpResponse(status=405)

	user = UserProfile.objects.get(id=id)
	test = UserAdaptiveTestLog.objects.filter(user = user, status = 'O').last()

	if not test:
		print "returned here 1"
		return HttpResponse(status=404)

	remaining_time = test.start_time - timezone.now() + timedelta(seconds=int(Config.get('test_total_time_in_seconds', 3600)))

	if answer_id == 0 or remaining_time.total_seconds() <= 0:
		UserAdaptiveTestAttemptLog.objects.filter(test = test).update(status='F')
		recompute_window_and_save(test, True, False)
		print "returned here 2"
		return JsonResponse({"test_score": test.score, "analytics": get_analytics(test)})

	answer = MCQAnswer.objects.get(id = answer_id)
	question = answer.question

	attempt = UserAdaptiveTestAttemptLog.objects.filter(test = test, question = question, status = 'W').first()
	
	if not attempt:
		print "returned here 3"
		return HttpResponse(status=404)

	attempt.answer = answer
	attempt.status = 'F'
	attempt.save()

	if test.question_remaining_in_set == 1:
		if test.set_remaining == 1:
			recompute_window_and_save(test, True, True)
			print "returned here 4"
			return JsonResponse({"test_score": test.score, "analytics": get_analytics(test)})
		recompute_window_and_save(test, False, True)
	else:
		test.question_remaining_in_set = test.question_remaining_in_set - 1
		test.save()

	if test.score <= 0 or test.score >= 100:
		print "returned here 5"
		return JsonResponse({"test_score": test.score, "analytics": get_analytics(test)})

	next_question = get_next_question(test)
	UserAdaptiveTestAttemptLog(test = test, question = next_question).save()

	question_json = MCQQuestionSerializer(next_question).data

	question_json['remaining_time_in_seconds'] = remaining_time.total_seconds()
	question_json['question_number'] = test.useradaptivetestattemptlog_set.count()

	#if test.score > int(Config.get('minimum_score_to_display_score', 80)):
	question_json['test_score'] = test.score

	print "returned here 6"
	return JsonResponse(question_json)


def recompute_window_and_save(test, is_end, is_attempted):
	total_number_of_set = int(Config.get('test_number_of_sets', 10))
	number_of_questions_in_sets = int(Config.get('number_of_questions_in_sets', 5))

	set_number = total_number_of_set - test.set_remaining + 1
	question_to_check = number_of_questions_in_sets - test.question_remaining_in_set
	if is_attempted:
		question_to_check = question_to_check + 1

	increment_window(test, set_number, question_to_check)

	test.question_remaining_in_set = 0 if is_end else number_of_questions_in_sets
	test.set_remaining = 0 if is_end else test.set_remaining - 1
	test.status = 'F' if is_end else 'O'

	test.save()

	UserAdaptiveTestScoreLog(test=test, set_number=set_number, score=test.score).save()


def increment_window(test, set_number, question_to_check):
	attempts = test.useradaptivetestattemptlog_set.select_related('question','answer').order_by("-start_time")[0 : question_to_check]
	set_score = calculate_set_score(attempts)
	print "set_score", set_score
	avg_person_score = float(Config.get('avg_person_score', 0.55))
	total_number_of_set = int(Config.get('test_number_of_sets', 10))
	initial_increment = int(Config.get('initial_window_increment', 15))
	final_increment = int(Config.get('final_window_increment', 5))
	incr = increment(avg_person_score, total_number_of_set, initial_increment, final_increment, set_score, set_number)
	test.window_start = test.window_start + incr
	test.window_end = test.window_end + incr


def increment(avg_person_score, total_number_of_set, initial_increment, final_increment, set_score, set_number):
    diff = set_score - avg_person_score
    numerator = (initial_increment - final_increment) * set_number - (initial_increment * total_number_of_set + final_increment)
    denominator = (1 - avg_person_score) * (1 - total_number_of_set)
    return (diff * numerator / denominator)


def calculate_set_score(attempts):
    summation = 0.0
    total_window_score = 0.0
    for attempt in attempts:
    	if attempt.answer and attempt.answer.correct:
    		attempt_time_taken = (attempt.end_time - attempt.start_time).total_seconds()
    		attempt_time_random = 2 * math.sqrt(20 * attempt.question.solvability + 250)
    		summation = summation + attempt.question.score * (attempt.question.initial_average_time + attempt_time_random) / (attempt_time_taken + attempt_time_random)
    	total_window_score = total_window_score + attempt.question.score
    return (summation / total_window_score) if total_window_score > 0 else 0.0


def get_next_question(test):
	solvability_min = 100 - test.window_end
	solvability_max = 100 - test.window_start
	attempted_questions = test.useradaptivetestattemptlog_set.values_list('question__id',flat=True)
	all_questions = MCQQuestion.objects.exclude(id__in = attempted_questions)\
		.filter(solvability__lte = solvability_max, solvability__gte = solvability_min)
	count = all_questions.count()
	while count == 0:
		solvability_min = solvability_min - 5
		solvability_max = solvability_max + 5
		all_questions = MCQQuestion.objects.exclude(id__in = attempted_questions)\
			.filter(solvability__lte = solvability_max, solvability__gte = solvability_min)
		count = all_questions.count()

	random_index = random.randint(0, count - 1)
	return all_questions[random_index]

def get_analytics(test):
	return UserAdaptiveTestScoreLogSerializer(test.useradaptivetestscorelog_set.order_by('set_number'), many=True).data
