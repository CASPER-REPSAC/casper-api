from rest_framework import serializers
from .models import Activity, Chapter, Chaptercomment, Chapterfile

#Activity
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields=('id','author','title','category')

class ActivityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields=('id','author','title','category')

#Chapter
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields=('activityid','subject','created_time','modified_time','article','filepath','filesize')

class ChapterListSerializer(serializers.ModelSerializer):
    activityid = ActivitySerializer(read_only=True)
    class Meta:
        model = Chapter
        fields=('activityid','chapterid','subject','created_time')

#Comment
class ChaptercommentSerializer(serializers.ModelSerializer):
    activityid = ActivitySerializer(read_only=True)
    chapterid = ChapterSerializer(read_only=True)

    class Meta:
        model = Chaptercomment 
        fields=('activityid','chapterid','commentpk','comment')

#Attachment
class ChapterfileSerializer(serializers.ModelSerializer):
    activityid = ActivitySerializer(read_only=True)
    chapterid = ChapterSerializer(read_only=True)

    class Meta:
        model = Chapterfile
        fields=('activityid','chapterid','filepk','filepath')