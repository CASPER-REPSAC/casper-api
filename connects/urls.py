from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from managing.views import activity_detail, activity_list, chapter_detail, chapter_update,ChapterViewSet
from managing.views import ActivityViewSet, FileView, APIView

admin.autodiscover()
urlpatterns = [

    url('admin/', admin.site.urls),

    # GET, POST uri

    path('api/activities/', activity_list),
    # 내쪽으로
    # path('api/activities/type/<str:filter_type>', activity_list),

    path('api/activities/<int:pk>/', activity_detail),

    # UPDATE uri
    path('api/activities/<int:pk>/chapter/<int:chapterid>/update_chapter/', chapter_update),

    # DELETE uri
    path('api/activities/<int:pk>/chapter/<int:chapterid>', chapter_detail),
    #path('api/activities/<int:pk>/chapter/<int:chapterid>/', chapter_detail),

    #Fileupload
    path('api/activities/<int:pk>/chapter/<int:chapterid>/upload/<str:filename>', FileView.as_view()), #

    path('api/', include('activity.urls')),
]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/registration', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),

]
