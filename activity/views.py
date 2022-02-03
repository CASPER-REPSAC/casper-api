from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from activity.models import *
from activity.serializers import *

from rest_framework.decorators import api_view
from rest_framework import viewsets
from connects.utils import *
from activity.serializers import *
from rest_framework import generics, mixins, views

from rest_framework import status
from accounts.models import SocialUser, UserReturn
from django.utils.html import escape

User = get_user_model()


class ActivityViewSet(viewsets.ModelViewSet):
    """
    <====== ActivityViewSet ======>
    url 가 따로 존재하는 participants 경우 HyperlinkedModelSerializer 에서 오류가 발생하여,
    ModelSerializer를 사용하였기에 id 값과 url 을 모두 표시하였음.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     addTagName(serializer.data, Tag)
        #     addUserName(serializer.data, UserReturn)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        addTagName(serializer.data, Tag)
        addUserName(serializer.data, UserReturn)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        user_instance = USER_AUTHORIZAION(request)
        serializer = ActivitySerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=user_instance)
            if 'tags' in request.data:
                activity_instance = Activity.objects.get(pk=serializer.data['id'])  # 방금 생성된 activity_instance 가져옴
                req_tags = request.data['tags']  # post 로 입력받은 태그 리스트
                exist_tags = [tag.name for tag in Tag.objects.all()]  # 존재하는 태그 가져옴
                for r_tag in req_tags:
                    if r_tag not in exist_tags:  # 없으면 태그 db 에 등록
                        Tag(name=r_tag).save()
                    tag_instance = Tag.objects.get(name=r_tag)  # 태그 인스턴스 찾아옴
                    ActivityTag(activity_id=activity_instance, tag_id=tag_instance).save()  # activity 랑 tag 연결
                ActivityParticipant(activity_id=activity_instance, user_id=user_instance).save()  # activity 랑 작성자 연결
                # 문제 발견, 태그 생성은 되는데 response 에 보이질 않음.
                serializer = ActivitySerializer(activity_instance, context=context)
                # 시리얼라이저를 재정의해서 데이터를 다시가져오는 것으로 해결.
                addTagName(serializer.data, Tag)
                addUserName(serializer.data, UserReturn)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        addTagName(serializer.data, Tag)
        addUserName(serializer.data, User)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        context = {'request': request}

        activity_instance = self.get_object()

        try:
            token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
            authed = token.decode_jwt()
            user_instance = User.objects.get(id=authed['user_id'])
            if activity_instance.author != user_instance.email:
                return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
        partial = kwargs.pop('partial', False)

        serializer = self.get_serializer(activity_instance, data=request.data, partial=partial, context=context)
        # # set partial=True to update a data partially

        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=user_instance.email,
                            title=escape(request.data['title']))
            # , description = escape(request.data['description']))

        if getattr(activity_instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            activity_instance._prefetched_objects_cache = {}
        deleted_participants = request.data['participants_delete']
        for i in deleted_participants:
            if (authed['user_id'] == i):
                pass
            else:
                part = ActivityParticipant.objects.get(user_id=i, activity_id=pk)
                try:
                    # print(type(part))
                    # If you get here, it exists...
                    part.delete()
                except:
                    pass
                    # Doesn't exist!
        pk = activity_instance.id
        if 'tags' in request.data:
            old_tags = ActivityTag.objects.filter(activity_id=pk)
            old_tags.delete()
            req_tags = request.data['tags']  # post 로 입력받은 태그 리스트
            exist_tags = [tag.name for tag in Tag.objects.all()]  # 존재하는 태그 가져옴

            for r_tag in req_tags:
                if r_tag not in exist_tags:  # 없으면 태그 db 에 등록
                    Tag(name=r_tag).save()
                tag_instance = Tag.objects.get(name=r_tag)  # 태그 인스턴스 찾아옴
                ActivityTag(activity_id=activity_instance, tag_id=tag_instance).save()  # activity 랑 tag 연결
            if not ActivityParticipant.objects.filter(activity_id=activity_instance, user_id=user_instance):
                ActivityParticipant(activity_id=activity_instance,
                                    user_id=user_instance).save()  # activity 랑 작성자 연결
            # 문제 발견, 태그 생성은 되는데 response 에 보이질 않음.
            serializer = ActivitySerializer(activity_instance, context=context)
            # 시리얼라이저를 재정의해서 데이터를 다시가져오는 것으로 해결.
            addTagName(serializer.data, Tag)
            #####end#####
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


#####################################################
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
