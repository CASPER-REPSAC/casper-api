from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from activity import views
from activity.views import ActivityViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView

# router를 생성하고 viewset을 등록한다
router = DefaultRouter()
router.register(r'activities', views.ActivityViewSet)
router.register(r'actitags', views.ActivityTagViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'actiparticipants', views.ActivityParticipantViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# API URL은 router에 의해 자동적으로 결정되어진다

urlpatterns = [
    # path('activities', views.ActivityViewSet),
    path('', include(router.urls)),
    # path('activities/', views.ActivityViewSet),
    # path('actitags/', views.ActivityTagViewSet),
    # path('tags/', views.TagViewSet),
    # path('api-auth/', include('rest_framework.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
]
