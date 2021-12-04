from rest_framework import serializers
from .models import Chapter, Chaptercomment, Chapterfile
from .serializers import *
from django.core.files import File
from rest_framework.serializers import ValidationError
from activity.models import *
from activity.serializers import Tag_IdSerializer, User_IdSerializer


# Comment
class ChaptercommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chaptercomment
        fields = ('activityid', 'chapterid', 'commentpk', 'comment')


# Attachment
class ChapterfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapterfile
        fields = ('activityid','chapterid', 'filepath','filename','fileext','file')

class ChapterfileListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapterfile
        fields =('filepk','activityid','chapterid', 'filepath','filename')


# Chapter
class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('activityid', 'chapterid', 'subject', 'created_time', 'last', 'next')


class ChapterSerializer(serializers.ModelSerializer):
    
    files = ChapterfileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chapter
        fields = (
            'activityid', 'chapterid', 'subject', 'created_time', 'modified_time', 'article', 'filepath', 'fileid',
            'last', 'next','files')


# Activity
class ActivityListSerializer(serializers.HyperlinkedModelSerializer):
    tags = Tag_IdSerializer(many=True, read_only=True)
    participants = User_IdSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ('url', 'id', 'title', 'type', 'author', 'createDate', 'description',
                  'startDate', 'endDate', 'currentState', 'viewerNum', 'tags', 'participants')


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    tags = Tag_IdSerializer(many=True, read_only=True)
    participants = User_IdSerializer(many=True, read_only=True)
    chapterid = ChapterListSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ('url', 'id', 'title', 'type', 'author', 'createDate', 'description',
                  'startDate', 'endDate', 'currentState', 'viewerNum', 'tags', 'participants', 'chapterid')
