from django.urls import path
from activity import views

urlpatterns = [
    path('activities/', views.activityList),
    path('activities/<int:pk>/', views.activityDetails),
]
