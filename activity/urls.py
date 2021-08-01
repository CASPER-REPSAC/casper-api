from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from activity import views

urlpatterns = [
    path('activities/', views.ActivityList().as_view()),
    path('activities/<int:pk>/', views.ActivityDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)