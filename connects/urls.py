from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from managing.views import activity_detail, activity_list,chapter_detail, chapter_update
from managing.views import ActivityViewSet

admin.autodiscover()
urlpatterns = [
    url('admin/', admin.site.urls),
    
    #GET, POST uri 
    #path('', activity_list),

    path('api/activities', activity_list),
    path('api/activities/', activity_list),
    path('api/activities/<int:pk>',activity_detail),
    path('api/activities/<int:pk>/',activity_detail),

    #UPDATE uri
    path('api/activities/<int:pk>/chapter/<int:chapterid>/update_chapter',chapter_update),
    #DELETE uri
    path('api/activities/<int:pk>/chapter/<int:chapterid>',chapter_detail), 
    path('api/activities/<int:pk>/chapter/<int:chapterid>/',chapter_detail),
    
    path('api/', include('activity.urls')),
]
