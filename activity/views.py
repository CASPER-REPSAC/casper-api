from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from activity.models import *
from activity.serializers import *
from rest_framework.decorators import api_view
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from connects.middleware import JWTValidation
from connects.utils import addTagName, addUserName


class ActivityViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    <====== ActivityViewSet ======>
    url 가 따로 존재하는 participants 경우 HyperlinkedModelSerializer 에서 오류가 발생하여,
    ModelSerializer를 사용하였기에 id 값과 url 을 모두 표시하였음.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def update(self, request, *args, **kwargs):
        try:
            authori = request.META['HTTP_AUTHORIZATION']
            token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
            authed = token.decode_jwt()
            user_instance = User.objects.get(id=authed['user_id'])  # .only("first_name","last_name")
        except:
            return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    


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
