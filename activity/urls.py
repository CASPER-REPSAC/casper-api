from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from activity import views
from activity.views import ActivityViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

# router를 생성하고 viewset을 등록한다
router = DefaultRouter()
router.register(r'activities', views.ActivityViewSet)
router.register(r'actitags', views.ActivityTagViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'actiparticipants', views.ActivityParticipantViewSet)

# API URL은 router에 의해 자동적으로 결정되어진다
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
