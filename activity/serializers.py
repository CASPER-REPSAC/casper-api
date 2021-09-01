from rest_framework import serializers
from activity.models import *

from django.contrib.auth.models import User, Group


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ActivityParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityParticipant
        fields = ['id', 'activity_id', 'user_id']


class ActivityTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityTag
        fields = ['id', 'activity_id', 'tag_id']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    acti = ActivityTagSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['url', 'id', 'name', 'acti']


class Tag_IdSerializer(serializers.HyperlinkedModelSerializer):
    # < 현재테이블 >.< FK인user컬럼 >.< 역참조관계명 >.all()
    name = ActivityTag.objects.select_related('tag_id')

    class Meta:
        model = ActivityTag
        fields = ['tag_id']


class User_IdSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityParticipant
        fields = ['user_id']


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    tags = Tag_IdSerializer(many=True, read_only=True)
    participants = User_IdSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['url', 'id', 'title', 'type', 'author', 'createDate', 'description',
                  'startDate', 'endDate', 'currentState', 'viewerNum', 'tags', 'participants']
