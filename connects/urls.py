from django.conf.urls import path, url, include
from django.contrib import admin
from managing.views import activity_detail, activity_list,chapter_detail
from managing.views import ActivityViewSet

admin.autodiscover()
urlpatterns = [
    url('admin/', admin.site.urls),
    
    #GET, POST uri 
    #path('', activity_list),
    path('api/', activity_list),
    path('api/', activity_list),
    path('api/<int:pk>',activity_detail),
    path('api/<int:pk>/',activity_detail),
    path('api/<int:pk>/<int:chapterid>',chapter_detail), 
    path('api/<int:pk>/<int:chapterid>/',chapter_detail),
    
    path('', include('activity.urls')),

    #PUT-PATCH uri
    #DELETE uri
]
