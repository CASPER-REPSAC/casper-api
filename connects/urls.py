from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from managing.views import activity_detail, activity_list,chapter_detail
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
    path('api/activities/<int:pk>/chapter/<int:chapterid>',chapter_detail), 
    path('api/activities/<int:pk>/chapter/<int:chapterid>/',chapter_detail),
    
    path('api/', include('activity.urls')),

    #PUT-PATCH uri
    #DELETE uri
]
