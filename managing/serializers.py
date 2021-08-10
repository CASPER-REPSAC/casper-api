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
        fields=('chapterid','subject','created_time','modified_time','article','filepath','filesize')

class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields=('chapterid','subject','created_time')

#Comment
class ChaptercommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chaptercomment 
        fields=('commentpk','comment')

#Attach
class ChapterfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapterfile
        fields=('filepk','filepath')