# from _typeshed import FileDescriptorLike
import datetime
import os
import re
import uuid
import json

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, QueryDict
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser  # for file upload
from rest_framework.response import Response
from rest_framework.views import APIView
from connects.middleware import JWTValidation
from connects.utils import addTagName, addUserName
from .models import Activity, Chapter, Chaptercomment, Chapterfile
from .serializers import *
from accounts.models import SocialUser, UserReturn
from activity.serializers import ActivitySerializer


# from django.contrib.auth.hashers import make_password, check_password


# # Activity

@api_view(['GET', 'POST'])
def activity_list(request):
    context = {'request': request}
    if request.method == "GET":
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True, context=context)
        addTagName(serializer.data, Tag)
        addUserName(serializer.data, UserReturn)
        return Response(serializer.data)

    elif request.method == "POST":
        try:
            authori = request.META['HTTP_AUTHORIZATION']
            token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
            authed = token.decode_jwt()
            user_instance = User.objects.get(id=authed['user_id'])
        except:
            return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
        serializer = ActivitySerializer(data=request.data, context=context)
        if serializer.is_valid():  # raise_exception=True):
            serializer.save(author=user_instance,
                            title=escape(request.data['title']))  # , description = escape(request.data['description']))
            if 'tags' in request.data:
                activity_instance = Activity.objects.get(pk=serializer.data['id'])  # 방금 생성된 activity_instance 가져옴
                req_tags = request.data['tags']  # post 로 입력받은 태그 리스트
                exist_tags = [tag.name for tag in Tag.objects.all()]  # 존재하는 태그 가져옴
                for r_tag in req_tags:
                    if r_tag not in exist_tags:  # 없으면 태그 db 에 등록
                        Tag(name=escape(r_tag)).save()
                    tag_instance = Tag.objects.get(name=r_tag)  # 태그 인스턴스 찾아옴
                    ActivityTag(activity_id=activity_instance, tag_id=tag_instance).save()  # activity 랑 tag 연결
                ActivityParticipant(activity_id=activity_instance, user_id=user_instance).save()  # activity 랑 작성자 연결
                # 문제 발견, 태그 생성은 되는데 response 에 보이질 않음.
                serializer = ActivitySerializer(activity_instance, context=context)
                # 시리얼라이저를 재정의해서 데이터를 다시가져오는 것으로 해결.
                addTagName(serializer.data, Tag)
                addUserName(serializer.data, UserReturn)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## Activity update
## Chapter Write
# @csrf_exempt
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def activity_detail(request, pk):
    context = {'request': request}
    if request.method == "GET":
        context = {'request': request}
        activity = Activity.objects.filter(id=pk)
        serializer = ActivityChapterSerializer(activity, many=True, context=context)

        ####start#####
        ### 공사중 ###
        addTagName(serializer.data, Tag)
        addUserName(serializer.data, UserReturn)
        ######end#####

        return Response(serializer.data)

    elif request.method == "POST":
        try:
            authori = request.META['HTTP_AUTHORIZATION']
            token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
            authed = token.decode_jwt()

            user_instance = User.objects.get(id=authed['user_id'])
            activity_instance = Activity.objects.get(id=pk, author=user_instance)

            if activity_instance is None:
                return Response({'error': 'Activity is Non-Existent'}, status=status.HTTP_400_BAD_REQUEST)
            if not check_password(request.data['authString'], activity_instance.authString):
                return Response({'error': 'invalid Auth-String'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'auth error'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            chapterLast = Chapter.objects.filter(activityid=pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(last=0,
                                subject=escape(request.data['subject']))  # , article=escape(request.data['article']))
            else:
                serializer.save(last=chapterLast.chapterid, subject=escape(request.data[
                                                                               'subject']))  # ,  article=escape(request.data['article']), subject = escape(request.data['subject']))
            chapterNow = Chapter.objects.filter(activityid=pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(next=0,
                                subject=escape(request.data['subject']))  # ,  article=escape(request.data['article']))
            else:
                serializer.save(next=chapterNow.chapterid, subject=escape(request.data[
                                                                              'subject']))  # ,  article=escape(request.data['article']), subject = escape(request.data['subject']))
                chapterLast.next = chapterNow.chapterid
                chapterLast.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        activity_instance = Activity.objects.get(pk=pk)
        try:
            token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
            authed = token.decode_jwt()
            user_instance = User.objects.get(id=authed['user_id'])
            if activity_instance.author != user_instance.email:
                return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
            if not check_password(request.data['authString'], activity_instance.authString):
                return Response({'error': 'invalid Auth-String'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'auth error'}, status=status.HTTP_400_BAD_REQUEST)

        deleted_participants = request.data['participants_delete']
        for i in deleted_participants:
            if (authed['user_id'] == i):
                pass
            else:
                part = ActivityParticipant.objects.get(user_id=i, activity_id=pk)
                try:
                    part.delete()
                except:
                    pass
        serializer = ActivitySerializer(instance=activity_instance, data=request.data, partial=True, context=context)
        # set partial=True to update a data partially
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data['authString'] = request.data['authString']
            serializer.update(instance=activity_instance, validated_data=validated_data)
            # 158 번줄 (윗줄)이 액티비티를 생성해벌임, (해결!)
            activity_instance = Activity.objects.get(pk=pk)
            if 'tags' in request.data:
                old_tags = ActivityTag.objects.filter(activity_id=pk)
                old_tags.delete()
                req_tags = request.data['tags']  # post 로 입력받은 태그 리스트
                exist_tags = [tag.name for tag in Tag.objects.all()]  # 존재하는 태그 가져옴
                for r_tag in req_tags:
                    if r_tag not in exist_tags:  # 없으면 태그 db 에 등록
                        Tag(name=escape(r_tag)).save()
                    tag_instance = Tag.objects.get(name=r_tag)  # 태그 인스턴스 찾아옴
                    ActivityTag(activity_id=activity_instance, tag_id=tag_instance).save()  # activity 랑 tag 연결
                if not ActivityParticipant.objects.filter(activity_id=activity_instance, user_id=user_instance):
                    ActivityParticipant(activity_id=activity_instance,
                                        user_id=user_instance).save()  # activity 랑 작성자 연결
                # 문제 발견, 태그 생성은 되는데 response 에 보이질 않음.
                serializer = ActivitySerializer(activity_instance, context=context)
                # 시리얼라이저를 재정의해서 데이터를 다시가져오는 것으로 해결.
                addTagName(serializer.data, Tag)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        activity_instance = Activity.objects.get(pk=pk)
        try:
            authori = request.META['HTTP_AUTHORIZATION']
            token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
            authed = token.decode_jwt()
            user_instance = User.objects.get(id=authed['user_id'])
            if activity_instance.author != user_instance.email:
                return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
        activity_instance.delete()
        return Response({'OK': 'ACTIVITY HAS DELETED'}, status=status.HTTP_200_OK)


## Chapter update
# @csrf_exempt
@api_view(['POST'])
def chapter_update(request, pk, chapterid):
    try:
        token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
        authed = token.decode_jwt()

        acti = Activity.objects.get(id=pk)
        user = User.objects.get(id=authed['user_id'])
        # print(acti.author)
        # print(len(acti.author))
        # print(user.email)
        # print(len(user.email))

        if (acti.author).strip() != (user.email).strip():
            # print('chapter_up')
            return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)

    except:
        # print("chapterupdate_here1")
        return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)

    if request.data['file_delete'] is not None:
        delete_f = request.data['file_delete']

        if len(delete_f) == 3:
            delete_ = Chapterfile.objects.filter(
                Q(filepath=delete_f[0]) | Q(filepath=delete_f[1]) | Q(filepath=delete_f[2]))
            delete_.delete()
            os.remove(settings.MEDIA_ROOT + "/" + delete_f[0])
            os.remove(settings.MEDIA_ROOT + "/" + delete_f[1])
            os.remove(settings.MEDIA_ROOT + "/" + delete_f[2])
        elif len(delete_f) == 2:
            delete_ = Chapterfile.objects.filter(Q(filepath=delete_f[0]) | Q(filepath=delete_f[1]))
            delete_.delete()
            os.remove(settings.MEDIA_ROOT + "/" + delete_f[0])
            os.remove(settings.MEDIA_ROOT + "/" + delete_f[1])
        elif len(delete_f) == 1:
            delete_ = Chapterfile.objects.filter(Q(filepath=delete_f[0]))
            delete_.delete()
            os.remove(settings.MEDIA_ROOT + "/" + delete_f[0])

        else:
            pass

    update_chapter = Chapter.objects.get(chapterid=chapterid)
    update_chapter.subject = request.data['subject']
    update_chapter.article = request.data['article']
    # update_chapter.subject = request.POST['subject']

    update_chapter.save()
    return Response(status=status.HTTP_200_OK)


## Chapter
# @csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def chapter_detail(request, pk, chapterid):
    try:
        chapter = Chapter.objects.filter(activityid=pk, chapterid=chapterid)
    except Chapter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        # return Response(serializer.data)

    if request.method == "GET":
        chapters = Chapter.objects.filter(activityid=pk, chapterid=chapterid)
        chapterfile = Chapterfile.objects.filter(activityid=pk, chapterid=chapterid).only("filepk", "filepath",
                                                                                          "filename")
        chaptercomment = Chaptercomment.objects.filter(activityid=pk, chapterid=chapterid)

        fserializer = ChapterfileListingSerializer(chapterfile, many=True)
        serializer = ChapterSerializer(chapters, many=True)
        cmtserializer = ChaptercommentListSerializer(chaptercomment, many=True)

        ret = list()
        ret.append(serializer.data[0])
        files = list()
        comments = list()
        returnDict = list(serializer.data[0])
        returnDict.append(fserializer.data)
        for i in fserializer.data:
            files.append(dict(i))
        ret.append(files)

        for i in range(len(cmtserializer.data)):
            k = cmtserializer.data[i]
            k['user'] = chaptercomment[i].writer.email

            _json = json.loads(str(SocialUser.objects.get(user=chaptercomment[i].writer).extra_data))
            _json.pop('verified_email')
            _json.pop('id')
            _json.pop('locale')

            k['profile'] = _json
            comments.append(k)

        ret.append(comments)
        try:
            return Response(ret, status=status.HTTP_200_OK)
        except:
            return status.HTTP_404_NOT_FOUND

    elif request.method == "POST":

        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            chapterLast = Chapter.objects.filter(activityid=pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(last=0,
                                subject=escape(request.data['subject']))  # ,  article=escape(request.data['article']))
            else:
                serializer.save(last=chapterLast.chapterid, subject=escape(request.data[
                                                                               'subject']))  # ,  article=escape(request.data['article']), subject = escape(request.data['subject']))
            chapterNow = Chapter.objects.filter(activityid=pk).order_by('chapterid').last()
            if chapterLast is None:
                serializer.save(next=0, subject=escape(request.data[
                                                           'subject']))  # , article=escape(request.data['article']), subject = escape(request.data['subject']))
            else:
                serializer.save(next=chapterNow.chapterid)
                chapterLast.next = chapterNow.chapterid
            chapterLast.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        try:
            authori = request.META['HTTP_AUTHORIZATION']
            token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
            authed = token.decode_jwt()

            acti = Activity.objects.get(id=pk)
            user = User.objects.get(id=authed['user_id'])

            if acti.author != user.email:
                # print('chapter_up')
                return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)

        except:
            # print("chapterupdate_here1")
            return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)

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
        if (chapterNext is None) and (chapterLast is None):
            pass

        elif (chapterNext is None):  # and serializerLast.is_valid(raise_exception=True):
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


## File Upload
ext_not_allowed = ('.php', '.asp', '.aspx', '.jsp', '.jspx', '.elf')


@method_decorator(csrf_exempt, name='dispatch')
class FileView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format=None, *args, **kwargs):

        acti_id = request.parser_context['kwargs']['pk']
        chap_id = request.parser_context['kwargs']['chapterid']

        if 'file' not in request.FILES:
            return Response('Empty Content', status=status.HTTP_400_BAD_REQUEST)

        f = request.FILES['file']

        savedName = f.name.replace(" ", "_")
        ext = os.path.splitext(f.name)[1]
        # print(ext)
        if ext in ext_not_allowed:
            return Response('EXT NOT ALLOWED', status=status.HTTP_400_BAD_REQUEST)

        newFilename = "%s.%s" % (uuid.uuid4(), ext.replace(".", ""))
        addAttr = request.data
        date = datetime.datetime.now()

        destination = open(settings.MEDIA_ROOT + "/" + newFilename, 'wb+')
        chucks = f.read()
        pattern = re.compile(b"(?<=\r\n\r\n)[\s\S]*(?=\r\n------WebKitFormBoundary)", re.S)
        # pattern = re.compile(b'\r\n\r\n[\s\S]+\r\n------WebKitFormBoundary', re.S)
        data = re.search(pattern, chucks)
        if data:
            destination.write(data.group())
        else:
            destination.write(chucks)
        destination.close()  # File should be closed only after all chuns are added

        # with open(settings.MEDIA_ROOT + "/" + newFilename, 'rb') as d_file:
        #     str_text = d_file.read()
        #     print(str_text)
        #
        #     print(data)
        addAttr['activityid'] = acti_id
        addAttr['chapterid'] = chap_id
        addAttr['filepath'] = newFilename  # file_path
        addAttr['filename'] = filename
        addAttr['fileext'] = ext
        addAttr['create_date'] = date
        addAttr['file'] = f
        addAttrDict = QueryDict('', mutable=True)
        addAttrDict.update(addAttr)
        fileSerializer = ChapterfileSerializer(data=addAttrDict)
        if fileSerializer.is_valid():
            fileSerializer.save()
            try:
                os.remove(settings.MEDIA_ROOT + "/" + savedName)
            except:
                pass
            return Response(status=status.HTTP_201_CREATED)
        else:
            try:
                os.remove(settings.MEDIA_ROOT + "/" + savedName)
            except:
                pass
            return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


## File Download
def getfile(request, pk, chapterid, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    content_types = {
        "zip": "application/zip",
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "pdf": "application/pdf",
        "ppt": "application/vnd.ms-powerpoint",
        "xls": "application/vnd.ms-excel",
        "7z": "application/x-7z-compressed",
        "gif": "image/gif",
        "others": "application/octet-stream"
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


class CommentView(APIView):
    def post(self, request):
        try:
            token = request.POST['access_token']
            JWT = JWTValidation(token.split()[1])
            pk = JWT.decode_jwt()
            if not pk:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                context = {'request': request}
                date = datetime.datetime.now()
                serializer = ChaptercommentSerializer(data=request.data, createtime=date)
                if serializer.is_valid(raise_exception=True):

                    serializer.save(writer=pk['user_id'])
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kargs):
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
                    context = {'request': request}
                    date = datetime.datetime.now()
                    serializer = ChaptercommentSerializer(data=request.data, createtime=date)
                    if serializer.is_valid(raise_exception=True):

                        serializer.save(writer=pk['user_id'])
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def write_comment(request):
    try:
        token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
        authed = token.decode_jwt()
    # return Response(authed, status=status.HTTP_400_BAD_REQUEST)
    except:
        # print("chapterupdate_here1")
        # return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)

    if not authed:
        return Response(authed, status=status.HTTP_400_BAD_REQUEST)

    context = {'request': request}
    # date = datetime.datetime.now()

    serializer = ChaptercommentWriteSerializer(data=request.data, )
    if serializer.is_valid(raise_exception=True):

        serializer.save(writer=User.objects.get(id=authed['user_id']))  # ,  comment=escape(request.data['comment']))
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_comment(request, commentpk):
    try:
        token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
        authed = token.decode_jwt()
        comment = Chaptercomment.objects.get(commentpk=commentpk, writer=authed['user_id'])
        comment.delete()
    except:
        # print("chapterupdate_here1")
        return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def search_all(request):
    try:
        keyword = request.GET.get('keyword', '')
        acti = Activity.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword)).distinct()
        chapter = Chapter.objects.filter(Q(article__icontains=keyword) | Q(subject__icontains=keyword)).distinct()

        acti_serializer = ActivitySerializer(acti, many=True, context={'request': request})
        chapter_serializer = ChapterSerializer(chapter, many=True, context={'request': request})
        addTagName(acti_serializer.data, Tag)
        addUserName(acti_serializer.data, User)

        search_type = request.GET.get('search_type')
        if search_type == 'activity':
            search = acti_serializer.data
        elif search_type == 'chapter':
            search = chapter_serializer.data
        else:
            search = acti_serializer.data + chapter_serializer.data
            search_type = 'all'

        # get query 로 페이지 번호와 페이지 크기를 입력받음
        page_size = int(request.GET.get('page_size', 10))
        page_number = int(request.GET.get('page_number', 1))

        paginator = Paginator(search, page_size)
        paginated_search = paginator.page(page_number).object_list
        ret = {"searched_objects_count": paginator.count,
               "page_size": page_size,  # 페이지 사이즈
               "page_index": page_number,  # 현재 페이지 번호
               "page_end_index": paginator.num_pages,  # 페이지 끝 번호
               "search_type": search_type,  # 검색 유형
               "searched_objects": paginated_search  # 검색 결과들
               }
        # 이게 더 간단함. 물론 이렇게 쓰는건 아닌 것 같지만, 일단 원하는 대로 작동은 함
        return Response(ret, status=status.HTTP_200_OK)
    except EmptyPage as e:
        return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({"error": "Input Value must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
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
