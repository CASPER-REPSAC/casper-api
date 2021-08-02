from django.shortcuts import render
from .serializers import ActivitySerializer, ChapterSerializer, ChapterarticleSerializer, ChaptercommentSerializer ,ChapterfileSerializer
from .models import Activity, Chapter, Chapterarticle, Chaptercomment, Chapterfile
from rest_framework import viewsets, permissions

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = (permissions.IsAuthenticated,)

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ChapterarticleViewSet(viewsets.ModelViewSet):
    queryset = Chapterarticle.objects.all()
    serializer_class = ChapterarticleSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ChaptercommentViewSet(viewsets.ModelViewSet):
    queryset = Chaptercomment.objects.all()
    serializer_class = ChaptercommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ChapterfileViewSet(viewsets.ModelViewSet):
    queryset = Chapterfile.objects.all()
    serializer_class = ChapterfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

