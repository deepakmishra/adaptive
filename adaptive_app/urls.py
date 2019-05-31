"""adaptive_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from problems import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^api/users/(?P<id>\d+)/tests', views.start_test),
	url(r'^api/users/(?P<id>\d+)/attempts', views.attempt_question),
	url(r'^api/users/(?P<id>\d+)', views.user_profile),
	url(r'^api/users/search', views.email_profile),
	url(r'^test', views.test_page),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
