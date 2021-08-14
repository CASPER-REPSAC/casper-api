from django.conf.urls import url, include
from django.contrib import admin

from managing.views import activity_detail, activity_list,chapter_detail
from managing.views import ActivityViewSet
from django.urls import path

urlpatterns = [
    url('admin/', admin.site.urls),
    
    #GET, POST uri 
    path('api/activities', activity_list),
    path('api/activities/', activity_list),
    path('api/activities/<int:pk>',activity_detail),
    path('api/activities/<int:pk>/',activity_detail),
    path('api/activities/<int:pk>/<int:chapterid>',chapter_detail), 
    path('api/activities/<int:pk>/<int:chapterid>/',chapter_detail),

    #PUT-PATCH uri

    #DELETE uri
]





"""connects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""