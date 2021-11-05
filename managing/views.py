# from _typeshed import FileDescriptorLike
from django.shortcuts import redirect, render, get_list_or_404
from django.http.request import QueryDict
import os

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser  # for file upload
from rest_framework import viewsets, serializers, status

from .serializers import ActivitySerializer, ChapterSerializer, ChapterListSerializer, ChaptercommentSerializer, \
    ChapterfileSerializer, ActivityListSerializer
# from activity.serializers import ActivitySerializer
from .models import Activity, Chapter, Chaptercomment, Chapterfile
from activity.models import *


def addTagName(response_data):
    tag_list = Tag.objects.all()
    print("태그 데이터 : ")
    for d_idx, _object in enumerate(response_data):
        for o_idx, tag in enumerate(_object['tags']):
            response_data[d_idx]['tags'][o_idx]['tag_name'] = str(tag_list.get(pk=tag['tag_id']))
    return response_data


def addUserName(response_data):
    user_list = AuthUser.objects.all()
    for d_idx, _object in enumerate(response_data):
        for o_idx, tag in enumerate(_object['participants']):
            response_data[d_idx]['participants'][o_idx]['user_name'] = str(user_list.get(pk=tag['user_id']))
    return response_data


@api_view(['GET', 'POST'])
def activity_list(request):
    context = {'request': request}
    if request.method == "GET":
        activities = Activity.objects.all()
        serializer = ActivityListSerializer(activities, many=True, context=context)
        ##########
        # 공사중 #
        ##########
        response_data = addTagName(serializer.data)
        response_data = addUserName(response_data)
        ##########
        # 공사중 #
        ##########
        return Response(response_data)

    elif request.method == "POST":
        serializer = ActivitySerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def activity_detail(request, pk):
    if request.method == "GET":
        context = {'request': request}
        activity = Activity.objects.filter(id=pk)
        serializer = ActivitySerializer(activity, many=True, context=context)
        return Response(serializer.data)

    elif request.method == "POST":
        context = {'request': request}
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            chapterLast = Chapter.objects.filter(activityid=pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(last=0)
            else:
                serializer.save(last=chapterLast.chapterid)
            chapterNow = Chapter.objects.filter(activityid=pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(next=0)
            else:
                serializer.save(next=chapterNow.chapterid)
                chapterLast.next = chapterNow.chapterid
            chapterLast.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    elif request.method == "POST":
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            chapterLast = Chapter.objects.filter(activityid = pk).order_by('chapterid').last()
            print(chapterLast.chapterid)
            serializer.last = chapterLast.chapterid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''


@api_view(['POST'])
def chapter_update(request, pk, chapterid):
    update_chapter = Chapter.objects.get(chapterid=chapterid)
    update_chapter.subject = request.POST['subject']
    update_chapter.article = request.POST['article']
    # update_chapter.subject = request.POST['subject']

    update_chapter.save()
    return redirect('detail', update_chapter.chapterid)


@api_view(['GET', 'POST', 'DELETE'])
def chapter_detail(request, pk, chapterid):
    try:
        chapter = Chapter.objects.filter(activityid=pk, chapterid=chapterid)
    except Chapter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        chapters = Chapter.objects.filter(activityid=pk, chapterid=chapterid)
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            chapterLast = Chapter.objects.filter(activityid=pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(last=0)
            else:
                serializer.save(last=chapterLast.chapterid)
            chapterNow = Chapter.objects.filter(activityid=pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(next=0)
            else:
                serializer.save(next=chapterNow.chapterid)
                chapterLast.next = chapterNow.chapterid
            chapterLast.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == "PUT":
    #    serializer = ChapterSerializer(data=request.data)
    #    if serializer.is_valid(raise_exception=True):
    #        serializer.save()
    #        return Response(serializer.data)

    elif request.method == "DELETE":
        # chapters = Chapter.objects.filter(activityid=pk)
        # serializer = ChapterSerializer(data=request.data)
        # print(dir(Chapter.objects))
        chapterLast = Chapter.objects.filter(activityid=pk, chapterid__lt=chapter.values('chapterid')).order_by(
            'chapterid').last()
        chapterNext = Chapter.objects.filter(activityid=pk, chapterid__gt=chapter.values('chapterid')).order_by(
            'chapterid').first()

        # serializerLast = ChapterSerializer(data=chapterLast.__dict__)
        # serializerNext = ChapterSerializer(data=chapterNext.__dict__)

        # print(dir(serializerNext))
        if chapterNext is None:  # and serializerLast.is_valid(raise_exception=True):
            chapterLast.next = 0
            chapterLast.save()

        elif (chapterLast is None):  # and serializerNext.is_valid(raise_exception=True):
            chapterNext.last = 0
            chapterNext.save()

        else:  # serializerLast.is_valid(raise_exception=True) and serializerNext.is_valid(raise_exception=True):
            chapterLast.next = chapterNext.chapterid
            chapterNext.last = chapterLast.chapterid
            chapterLast.save()
            chapterNext.save()

        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, req, *arg, **kwargs):
        activityid = 
        chapterid =
        filepk =
        filedata = req.data.dict()
        filename = req.data['file_name']
        filetype = os.path.splitext(filename.name)[1]
        saved_filename = file_upload_path(filename.name)
        filepath = '\\'.join()
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
