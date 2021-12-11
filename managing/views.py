# from _typeshed import FileDescriptorLike
import os, datetime, uuid, json
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_list_or_404
from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils.encoding import filepath_to_uri
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.files import File

from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser  # for file upload
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, serializers, status

from django.conf import settings
from connects.middleware import JWTValidation
from connects.utils import addTagName, addUserName
from activity.serializers import TagSerializer
from activity.models import *
from .serializers import *
from .models import Activity, Chapter, Chaptercomment, Chapterfile
from .utils import RandomFileName 
import uuid, collections


@csrf_exempt
@api_view(['GET', 'POST'])
def activity_list(request):
    context = {'request': request}
    if request.method == "GET":
        activities = Activity.objects.all()
        serializer = ActivityListSerializer(activities, many=True, context=context)

        ####start#####
        ### 공사중 ###
        addTagName(serializer.data, Tag)
        addUserName(serializer.data, User)
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
                addTagName(serializer.data, Tag)
            ######end#####

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'POST'])
def activity_detail(request, pk):
    if request.method == "GET":
        context = {'request': request}
        activity = Activity.objects.filter(id=pk)
        serializer = ActivitySerializer(activity, many=True, context=context)

        ####start#####
        ### 공사중 ###
        addTagName(serializer.data, Tag)
        addUserName(serializer.data,User)
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

@csrf_exempt
@api_view(['POST'])
def chapter_update(request, pk, chapterid):
    update_chapter = Chapter.objects.get(chapterid=chapterid)
    update_chapter.subject = request.POST['subject']
    update_chapter.article = request.POST['article']
    # update_chapter.subject = request.POST['subject']

    update_chapter.save()
    return redirect('detail', update_chapter.chapterid)

@csrf_exempt
@api_view(['GET', 'POST','DELETE'])
def chapter_detail(request, pk, chapterid):
    try:
        chapter = Chapter.objects.filter(activityid=pk,chapterid=chapterid)
    except Chapter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        chapters = Chapter.objects.filter(activityid=pk,chapterid=chapterid)
        chapterfile = Chapterfile.objects.filter(activityid=pk,chapterid=chapterid).only("filepk","filepath","filename")
        chaptercomment = Chaptercomment.objects.filter(activityid=pk, chapterid=chapterid)

        fserializer = ChapterfileListingSerializer(chapterfile, many=True)
        serializer = ChapterSerializer(chapters, many=True)
        cmtserializer = ChaptercommentListSerializer(chaptercomment, many=True)

        #print(serializer.data)
        ret = list()
        ret.append(serializer.data[0])
        files = list()
        comments = list()
        returnDict = list(serializer.data[0])
        returnDict.append(fserializer.data)
        for i in fserializer.data:
            files.append(dict(i))
        ret.append(files)

        for i in cmtserializer.data:
            comments.append(dict(i))
            
        ret.append(comments)
        return Response(ret)
        #return Response(serializer.data)

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


@method_decorator(csrf_exempt,name='dispatch')
class FileView(APIView):

    parser_classes = (FileUploadParser,)
    
    def post(self, request, filename, format=None, *args, **kwargs):

        if 'file' not in request.FILES:
            raise ParseError("Empty content")

        f = request.FILES['file']
        savedName = f.name.replace(" ","_")
        ext = os.path.splitext(f.name)[1]
        newFilename = "%s.%s" % (uuid.uuid4(), ext.replace(".",""))
        addAttr = request.data
        date = datetime.datetime.now()

        destination = open(settings.MEDIA_ROOT + "/" + newFilename, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()  # File should be closed only after all chuns are added
        
        addAttr['activityid'] = request.parser_context['kwargs']['pk']
        addAttr['chapterid'] = request.parser_context['kwargs']['chapterid']
        addAttr['filepath'] =  newFilename #file_path
        addAttr['filename'] = filename
        addAttr['fileext'] = ext
        addAttr['create_date'] = date
        addAttr['file'] = f
        addAttrDict = QueryDict('', mutable=True)
        addAttrDict.update(addAttr)

        fileSerializer = ChapterfileSerializer(data = addAttrDict)
        if fileSerializer.is_valid():
            
            fileSerializer.save()       

            os.remove(settings.MEDIA_ROOT + "/" + savedName)
 
            return Response(status=status.HTTP_201_CREATED)
        else:
            os.remove(settings.MEDIA_ROOT + "/" + savedName)

            return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)   


def getfile(request, pk, chapterid, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    #validated = dict()
    
    content_types = { 
        "zip" : "application/zip",
        "jpeg" :"image/jpeg",
        "jpg" : "image/jpeg",
        "pdf" : "application/pdf",
        "ppt" :"application/vnd.ms-powerpoint",
        "xls" :"application/vnd.ms-excel",
        "7z" : "application/x-7z-compressed",
        "gif" : "image/gif",
        "others" :"application/octet-stream"
        }
    c = content_types["others"]
    if filename.split(".")[1] in content_types:
        c = content_types[filename.split(".")[1]]
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=c)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)  
    #file = Chapterfile.objects.filter(activityid = pk,chapterid = chapterid, filepath = filename)
    #validated['file'] = File(open('home/flood/casper-api/files/' + filename))

    #return validated 



class CommentView(APIView):
    
    def post(self,request):
        try:
            token = request.POST['access_token']
            JWT = JWTValidation(token.split()[1])
            pk = JWT.decode_jwt()
            if not pk:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                context={'request': request}
                date = datetime.datetime.now()
                serializer = ChaptercommentSerializer(data=request.data,createtime=date)
                if serializer.is_valid(raise_exception=True):

                    serializer.save(writer = pk['writer'])
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST) 
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,**kargs):
        if kargs.get('commentpk') is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                token = request.POST['access_token']
                JWT = JWTValidation(token.split()[1])
                pk = JWT.decode_jwt()
                if not pk:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    context={'request': request}
                    date = datetime.datetime.now()
                    serializer = ChaptercommentSerializer(data=request.data,createtime=date)
                    if serializer.is_valid(raise_exception=True):

                        serializer.save(writer = pk['writer'])
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST) 
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def write_comment(request):

    try:
        token = request.POST['access_token']
        JWT = JWTValidation(token.split()[1])
        pk = JWT.decode_jwt()
        if not pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            context={'request': request}
            date = datetime.datetime.now()
            serializer = ChaptercommentSerializer(data=request.data,createtime=date)
            if serializer.is_valid(raise_exception=True):

                serializer.save(writer = pk['writer'])
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST) 
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST) 



@api_view(['POST'])
def delete_comment(request, commentpk):
    try:
        token = request.POST['access_token']
        JWT = JWTValidation(token.split()[1])
        pk = JWT.decode_jwt()
        pk = True
        if not pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            comment = Chaptercomment.objects.get(commentpk = commentpk)
            comment.delete()
            return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST) 



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
