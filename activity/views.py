from activity.models import Activity, ActivityTag, Tag, ActivityParticipant
from activity.serializers import *
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ActivityViewSet(viewsets.ModelViewSet):
    """
    <====== ActivityViewSet ======>
    url 가 따로 존재하는 participants 경우 HyperlinkedModelSerializer 에서 오류가 발생하여,
    ModelSerializer를 사용하였기에 id 값과 url 을 모두 표시하였음.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    <====== TagViewSet ======>
    url : 해당 Tag의 Deatail url
    name : 해당 Tag의 이름
    acti : 해당 Tag가 사용된 Activity
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ActivityTagViewSet(viewsets.ModelViewSet):
    """
    <====== ActivityTagViewSet ======>
    url 가 따로 존재하는 경우 -> HyperlinkedModelSerializer 에서 오류가 발생하여,
    ModelSerializer를 사용하였기에 id 값과 url 을 모두 표시하였음.
    """
    queryset = ActivityTag.objects.all()
    serializer_class = ActivityTagSerializer


class ActivityParticipantViewSet(viewsets.ModelViewSet):
    queryset = ActivityParticipant.objects.all()
    serializer_class = ActivityParticipantSerializer
