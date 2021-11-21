# from _typeshed import FileDescriptorLike
import os, datetime, uuid, json

from django.shortcuts import redirect, render, get_list_or_404
from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils.encoding import filepath_to_uri
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser  # for file upload
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, serializers, status

from connects import settings
from activity.serializers import TagSerializer
from activity.models import *
from .serializers import *
from .models import Activity, Chapter, Chaptercomment, Chapterfile





####start#####
### 공사중 ###
def addTagName(response_data):
    tag_list = Tag.objects.all()
    # post 로 생성할 때는 response_data 의 데이터 타입이 다름.
    # get 으로 불러올 떄는 ReturnDict 가 list 로 묶여있어서 ReturnList 이 되나봄.
    # 그래서 아래와 같이 따로 처리 해줌.
    if type(response_data) == ReturnDict:
        for o_idx, tag_id in enumerate(response_data['tags']):
            response_data['tags'][o_idx]['tag_name'] = str(tag_list.get(pk=tag_id['tag_id']))
    else:
        for d_idx, _object in enumerate(response_data):
            for o_idx, tag in enumerate(_object['tags']):
                response_data[d_idx]['tags'][o_idx]['tag_name'] = str(tag_list.get(pk=tag['tag_id']))
    # return response_data # 리턴이 없어도 serializer.data 가 수정됨.


def addUserName(response_data):
    user_list = AuthUser.objects.all()
    for d_idx, _object in enumerate(response_data):
        for o_idx, tag in enumerate(_object['participants']):
            response_data[d_idx]['participants'][o_idx]['user_name'] = str(user_list.get(pk=tag['user_id']))
    # return response_data # 리턴이 없어도 serializer.data 가 수정됨.
######end#####


@api_view(['GET', 'POST'])
def activity_list(request):
    context = {'request': request}
    if request.method == "GET":
        activities = Activity.objects.all()
        serializer = ActivityListSerializer(activities, many=True, context=context)

        ####start#####
        ### 공사중 ###
        addTagName(serializer.data)
        addUserName(serializer.data)
        ######end#####

        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ActivityListSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            ####start#####
            ### 공사중 ###
            if 'tags' in request.data:
                activity_instance = Activity.objects.get(pk=serializer.data['id']) # 방금 생성된 activity_instance 가져옴
                req_tags = request.data['tags']  # post 로 입력받은 태그 리스트
                exist_tags = [tag.name for tag in Tag.objects.all()]  # 존재하는 태그 가져옴
                for r_tag in req_tags:
                    if r_tag not in exist_tags:  # 없으면 태그 db 에 등록
                        Tag(name=r_tag).save()
                    tag_instance = Tag.objects.get(name=r_tag)  # 태그 인스턴스 찾아옴
                    ActivityTag(activity_id=activity_instance, tag_id=tag_instance).save()  # activity 랑 tag 연결
                # 문제 발견, 태그 생성은 되는데 response 에 보이질 않음.
                serializer = ActivityListSerializer(activity_instance, context=context)
                # 시리얼라이저를 재정의해서 데이터를 다시가져오는 것으로 해결.
                addTagName(serializer.data)
            ######end#####

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def activity_detail(request, pk):
    if request.method == "GET":
        context = {'request': request}
        activity = Activity.objects.filter(id=pk)
        serializer = ActivitySerializer(activity, many=True, context=context)

        ####start#####
        ### 공사중 ###
        addTagName(serializer.data)
        addUserName(serializer.data)
        ######end#####

        return Response(serializer.data)

    elif request.method == "POST":
        context={'request': request}
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            chapterLast = Chapter.objects.filter(activityid = pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(last = 0)
            else:
                serializer.save(last = chapterLast.chapterid)
            chapterNow = Chapter.objects.filter(activityid = pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(next = 0)
            else:
                serializer.save(next = chapterNow.chapterid)
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


@api_view(['GET', 'POST','DELETE'])
def chapter_detail(request, pk, chapterid):
    try:
        chapter = Chapter.objects.filter(activityid=pk,chapterid=chapterid)
    except Chapter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        chapters = Chapter.objects.filter(activityid=pk,chapterid=chapterid)
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            chapterLast = Chapter.objects.filter(activityid = pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(last = 0)
            else:
                serializer.save(last = chapterLast.chapterid)
            chapterNow = Chapter.objects.filter(activityid = pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(next = 0)
            else:
                serializer.save(next = chapterNow.chapterid)
                chapterLast.next = chapterNow.chapterid
            chapterLast.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #elif request.method == "PUT":
    #    serializer = ChapterSerializer(data=request.data)
    #    if serializer.is_valid(raise_exception=True):
    #        serializer.save()
    #        return Response(serializer.data)

    elif request.method == "DELETE":
        #chapters = Chapter.objects.filter(activityid=pk)
        #serializer = ChapterSerializer(data=request.data)
        #print(dir(Chapter.objects))
        chapterLast = Chapter.objects.filter(activityid = pk, chapterid__lt=chapter.values('chapterid')).order_by('chapterid').last()
        chapterNext = Chapter.objects.filter(activityid = pk, chapterid__gt=chapter.values('chapterid')).order_by('chapterid').first()

        #serializerLast = ChapterSerializer(data=chapterLast.__dict__)
        #serializerNext = ChapterSerializer(data=chapterNext.__dict__)

        #print(dir(serializerNext))
        if chapterNext is None:#and serializerLast.is_valid(raise_exception=True):
            chapterLast.next = 0
            chapterLast.save()

        elif (chapterLast is None): # and serializerNext.is_valid(raise_exception=True):
            chapterNext.last = 0
            chapterNext.save()

        else: # serializerLast.is_valid(raise_exception=True) and serializerNext.is_valid(raise_exception=True):
            chapterLast.next = chapterNext.chapterid
            chapterNext.last = chapterLast.chapterid
            chapterLast.save()
            chapterNext.save()

        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileView(APIView):

    parser_classes = (FileUploadParser,)

    def post(self, request,filename, format=None, *args, **kwargs):

        if 'file' not in request.FILES:
            raise ParseError("Empty content")

        f = request.FILES['file']
        #print(f)
        #print(dir(request))
        #print(request.__dict__)

        addAttr = request.data
        #file_name = request.data['filename']
        
        #new_file_full_name = file_upload_path(file_name.name)
        #file_path = '/'.join(new_file_full_name.split('/')[0:-1])
        date = datetime.datetime.now()
        print(date, datetime.datetime.now())
        #model Attr
        addAttr['activityid'] = request.parser_context['kwargs']['pk']
        addAttr['chapterid'] = request.parser_context['kwargs']['chapterid']
        addAttr['filepath'] = '/' #file_path
        addAttr['filename'] = filename
        addAttr['fileext'] = 'pdf' #os.path.splitext(file_name.name)[1]
        addAttr['create_date'] = date
        addAttr['file'] = f
        addAttrDict = QueryDict('', mutable=True)
        addAttrDict.update(addAttr)

        fileSerializer = ChapterfileSerializer(data = addAttrDict)
        if fileSerializer.is_valid():
            
            fileSerializer.save()       
            print(fileSerializer.data)

            return Response(status=status.HTTP_201_CREATED)
        else:
            print(fileSerializer.errors)
            return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)   


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
