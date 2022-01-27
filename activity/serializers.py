from rest_framework import serializers
from activity.models import *
from accounts.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


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
    auth_string = serializers.CharField(
        # write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        # style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        validated_data['auth_string'] = make_password(validated_data.get('auth_string'))
        return super(ActivitySerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['auth_string'] = make_password(validated_data.get('auth_string'))
        return super(ActivitySerializer, self).create(validated_data)

    class Meta:
        model = Activity
        fields = ('url', 'id', 'title', 'type', 'author', 'createDate', 'description',
                  'startDate', 'endDate', 'currentState', 'viewerNum', 'tags', 'participants', 'auth_string')


class Acti_IdSerializer(serializers.ModelSerializer):
    # < 현재테이블 >.< FK인user컬럼 >.< 역참조관계명 >.all()
    name = ActivityParticipant.objects.select_related('acti')

    class Meta:
        model = ActivityParticipant
        fields = ['user_id']


class UserSerializer(serializers.ModelSerializer):
    User = get_user_model()
    # activity_id = Acti_IdSerializer(many=True, read_only=True)
    acti = ActivityParticipant.objects.select_related('acti')

    class Meta:
        model = User
        fields = ('id', 'email', 'acti')
