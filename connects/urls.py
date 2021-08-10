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

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from managing.views import ActivityViewSet, ChapterViewSet, ChaptercommentViewSet, ChapterfileViewSet
from django.urls import path

router = routers.DefaultRouter()
router.register('activities',ActivityViewSet)
router.register('chapters',ChapterViewSet)
router.register('chaptercomments',ChaptercommentViewSet)
router.register('chapterfiles',ChapterfileViewSet)

urlpatterns = [
    #url('admin/', admin.site.urls),
    url(r'^',include(router.urls)),
    #GET uri
    path('activities/', ),
    path('activities/<int:id>',)
    #path('activities',___), #액티비티 목록 조회
    #path('activities/<int:activityid>',___), #특정 액티비티 조회
    #path('activities/<int:activityid>/chapters',___), #특정 액티비티의 챕터 목록 조회
    #path('activities/<int:activityid>/chapters/<int:chapterid>',___), #특정 액티비티의 특정 챕터 조회
    #path('activities/<int:activityid>/chapters/<int:chapterid>/comment/<int:comment_pk>',___), #특정 액티비티-챕터의 댓글 목록 조회

    #POST uri

    #PUT-PATCH uri

    #DELETE uri
]