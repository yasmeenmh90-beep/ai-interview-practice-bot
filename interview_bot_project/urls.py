from django.urls import path, include

urlpatterns = [
    path('', include('interview_bot.urls')),
]
