from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from activity import views

urlpatterns = [
    path('activities/', views.activityList),
    path('activities/<int:pk>/', views.activityDetail),
]
urlpatterns = format_suffix_patterns(urlpatterns)