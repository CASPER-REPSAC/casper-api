from django.shortcuts import render, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, serializers

from .serializers import ActivitySerializer, ActivityListSerializer, ChapterSerializer, ChapterListSerializer, ChaptercommentSerializer, ChapterfileSerializer
from .models import Activity, Chapter, Chaptercomment, Chapterfile


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    @api_view(['GET', 'POST'])
    def activity_list(request):
        if request.method == "GET":
            activities = get_list_or_404(Activity)
            serializer = ActivityListSerializer(activities, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = ActivitySerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    @api_view(['GET', 'POST'])
    def chapter_list(request):
        if request.method == "GET":
            chapters = get_list_or_404(Chapter)
            serializer = ChapterListSerializer(chapters, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = ChapterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

class ChaptercommentViewSet(viewsets.ModelViewSet):
    queryset = Chaptercomment.objects.all()
    serializer_class = ChaptercommentSerializer

class ChapterfileViewSet(viewsets.ModelViewSet):
    queryset = Chapterfile.objects.all()
    serializer_class = ChapterfileSerializer
