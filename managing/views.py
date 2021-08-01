from django.shortcuts import render
from .serializers import ActivitySerializer, ChapterSerializer, ChapterarticleSerializer, ChaptercommentSerializer ,ChapterfileSerializer
from .models import Activity, Chapter, Chapterarticle, Chaptercomment, Chapterfile
from rest_framework import viewsets

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class ChapterarticleViewSet(viewsets.ModelViewSet):
    queryset = Chapterarticle.objects.all()
    serializer_class = ChapterarticleSerializer

class ChaptercommentViewSet(viewsets.ModelViewSet):
    queryset = Chaptercomment.objects.all()
    serializer_class = ChaptercommentSerializer

class ChapterfileViewSet(viewsets.ModelViewSet):
    queryset = Chapterfile.objects.all()
    serializer_class = ChapterfileSerializer

