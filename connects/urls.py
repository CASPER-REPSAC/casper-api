from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from managing.views import activity_detail, activity_list, chapter_detail, chapter_update, ChapterViewSet
from managing.views import ActivityViewSet, FileView, APIView, getfile
from accounts.views import *

admin.autodiscover()


urlpatterns = [
    url('admin/', admin.site.urls),
    # GET, POST uri
    # path('', activity_list),
    # path('api/w00/activities', activity_list),
    #path('api/w00/activities/', ActivityViewSet),
    #path('api/activities', activity_list),
    path('api/activities/', activity_list),
    path('api/activities/<int:pk>', activity_detail),
    path('api/activities/<int:pk>/', activity_detail),

    # UPDATE uri
    path('api/activities/<int:pk>/chapter/<int:chapterid>/update_chapter/', chapter_update),

    # DELETE uri
    path('api/activities/<int:pk>/chapter/<int:chapterid>', chapter_detail),
    path('api/activities/<int:pk>/chapter/<int:chapterid>/', chapter_detail),

    #File
    path('api/activities/<int:pk>/chapter/<int:chapterid>/upload/<str:filename>/', FileView.as_view()), #
    path('api/activities/<int:pk>/chapter/<int:chapterid>/download/<str:filename>/', getfile),

    #Comment
    path('api/activities/write_comment/', ),
    path('api/activities/delete_comment/', ),

    #Activity
    path('api/w00/', include('activity.urls')),

    #JWT Verify
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #OAuth
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
]