from rest_framework import serializers
from .models import Activity, Chapter, Chaptercomment, Chapterfile

#Comment
class ChaptercommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chaptercomment 
        fields=('activityid','chapterid','commentpk','comment')

#Attachment
class ChapterfileSerializer(serializers.ModelSerializer):
    #activityid = ActivitySerializer(read_only=True)
    #chapterid = ChapterSerializer(read_only=True)

    class Meta:
        model = Chapterfile
        fields=('activityid','chapterid','filepk','filepath')

#Chapter
class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields=('activityid','chapterid','subject','created_time')

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields=('activityid','chapterid','subject','created_time','modified_time','article','filepath','filesize')

#Activity
class ActivityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields=('id','author','title','category')

class ActivitySerializer(serializers.ModelSerializer):
    chapterid = ChapterListSerializer(many=True, read_only=True)
    class Meta:
        model = Activity
        fields=('chapterid','id','author','title','category')