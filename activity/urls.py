from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from activity import views
from activity.views import ActivityViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter


# activity_list = ActivityViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# activity_detail = ActivityViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# urlpatterns = [
#     path('activities/', activity_list, name='activity-list'),
#     path('activities/<int:pk>/', activity_detail, name='activity-detail'),
#     # path('users/', views.UserList.as_view()),
#     # path('users/<int:pk>/', views.UserDetail.as_view()),
#     path('', views.api_root),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)




# router를 생성하고 viewset을 등록한다
router = DefaultRouter()
router.register(r'activities', views.ActivityViewSet)
router.register(r'actitags', views.ActivityTagViewSet)
router.register(r'tags', views.TagViewSet)
# router.register(r'users', views.UserViewSet)

# API URL은 router에 의해 자동적으로 결정되어진다
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]