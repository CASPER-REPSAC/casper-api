from django.shortcuts import render, get_list_or_404

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, serializers, status

from .serializers import ActivitySerializer, ActivityListSerializer, ChapterSerializer, ChapterListSerializer, ChaptercommentSerializer, ChapterfileSerializer
from .models import Activity, Chapter, Chaptercomment, Chapterfile

@api_view(['GET', 'POST'])
def activity_list(request):
    if request.method == "GET":
        activities = Activity.objects.all()
        serializer = ActivityListSerializer(activities, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def activity_detail(request, pk):
    if request.method == "GET":
        chapter = Chapter.objects.get(activityid=pk)
        serializer = ChapterListSerializer(chapter, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST','PUT','DELETE'])
def chapter_detail(request, pk):
    try:
        chapter = Chapter.objects.get(chapterid=pk)
    except Chapter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        chapters = Chapter.objects.all()
        serializer = ChapterListSerializer(chapters, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class ChaptercommentViewSet(viewsets.ModelViewSet):
    queryset = Chaptercomment.objects.all()
    serializer_class = ChaptercommentSerializer

class ChapterfileViewSet(viewsets.ModelViewSet):
    queryset = Chapterfile.objects.all()
    serializer_class = ChapterfileSerializer
'''
