from rest_framework import serializers
from activity.models import *
from accounts.models import User
from django.contrib.auth.models import User, Group
from accounts.serializers import UsersSerializer as Ac_UserSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'email')  # , 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ActivityParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityParticipant
        fields = ['id', 'activity_id', 'user_id']


class ActivityTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityTag
        fields = ['url', 'id', 'activity_id', 'tag_id']


class TagSerializer(serializers.ModelSerializer):
    acti = ActivityTagSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['url', 'id', 'name', 'acti']


class Tag_IdSerializer(serializers.ModelSerializer):
    # < 현재테이블 >.< FK인user컬럼 >.< 역참조관계명 >.all()
    name = ActivityTag.objects.select_related('tag_id')

    class Meta:
        model = ActivityTag
        fields = ['tag_id']


class User_IdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityParticipant
        fields = ['user_id']


class ActivitySerializer(serializers.ModelSerializer):
    tags = Tag_IdSerializer(many=True, read_only=True)
    participants = User_IdSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['url', 'id', 'title', 'type', 'author', 'createDate', 'description',
                  'startDate', 'endDate', 'currentState', 'viewerNum', 'tags', 'participants']
