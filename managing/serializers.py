from rest_framework import serializers
from .models import Activity, Chapter, Chaptercomment, Chapterfile

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields=('activityname','activitytype','activityid')

class ChapterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    subject = serializers.CharField(max_length=32)
    created = serializers.DateTimeField()
    article = serializers.CharField(max_length=500)

    def create(self, validated_data):
        return Chapter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.subject = '__INPUT_HERE__'
        instance.article = '__INPUT_HERE__'
        return instance

    class Meta:
        model = Chapter
        fields=('activityid','chapterid','chaptersubject','chaptercreated','chapterarticle')

class ChaptercommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chaptercomment 
        fields=('activityid','chapterid','commentcreated','comment')

class ChapterfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapterfile
        fields=('activityid','chapterid','filepath','filename')