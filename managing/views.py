from django.shortcuts import render
from .serializers import ActivitySerializer, ChapterSerializer, ChaptercommentSerializer ,ChapterfileSerializer
from .models import Activity, Chapter, Chaptercomment, Chapterfile
from rest_framework import viewsets, permissions

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class ChaptercommentViewSet(viewsets.ModelViewSet):
    queryset = Chaptercomment.objects.all()
    serializer_class = ChaptercommentSerializer

class ChapterfileViewSet(viewsets.ModelViewSet):
    queryset = Chapterfile.objects.all()
    serializer_class = ChapterfileSerializer
