from rest_framework import serializers
from activity.models import *


# # ModelSerializer_Version
class ActivityParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityParticipant
        fields = ['url', 'id', 'activity_id', 'user_id']


# class ActivityTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ActivityTag
#         fields = ['id', 'activity_id', 'tag_id']
#
#
# class TagSerializer(serializers.ModelSerializer):
#     acti = ActivityTagSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Tag
#         fields = ['id', 'name', 'acti']
#
#
# class Tag_IdSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ActivityTag
#         fields = ['tag_id']
#
#
# class ActivitySerializer(serializers.ModelSerializer):
#     tags = Tag_IdSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Activity
#         fields = ['id', 'title', 'type', 'author', 'createDate', 'introduce',
#                   'startDate', 'endDate', 'currentState', 'viewerNum', 'tags']


# HyperlinkedModelSerializer_Version
# class ActivityParticipantSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ActivityParticipant
#         fields = ['url', 'id', 'activity_id', 'user_id']


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
    class Meta:
        model = ActivityTag
        fields = ['tag_id']


class User_IdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityParticipant
        fields = ['url', 'user_id']


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    tags = Tag_IdSerializer(many=True, read_only=True)
    participants = User_IdSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['url', 'id', 'title', 'type', 'author', 'createDate', 'introduce',
                  'startDate', 'endDate', 'currentState', 'viewerNum', 'tags', 'participants']
