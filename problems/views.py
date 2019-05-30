from django.shortcuts import render
from problems.models import UserProfile
from problems.serializers import UserProfileSerializer
from django.http import JsonResponse, HttpResponse

def user_profile(request, id):
	user = UserProfile.objects.get(id=id)
	user_json = UserProfileSerializer(user).data
	return JsonResponse(user_json)

def start_test(request, id):
	user = UserProfile.objects.get(id=id)
	if not user.eligible:
		return HttpResponse(status=412, reason="Not Eligible")
	return HttpResponse(status=200)

def attempt_question(request, id):
	if request.method == 'GET':
		return HttpResponse(status=405)
	elif request.method == 'POST':
		pass