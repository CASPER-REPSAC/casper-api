from rest_framework import serializers
from .models import Activity, Chapter, Chapterarticle, Chaptercomment, Chapterfile

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields=('activityname','activitytype','activityid')

class ChapterSerializer(serializers.ModelSerializer):
    #activityid =

    def create(self, validated_data):
        return Chapter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #
        return instance

    class Meta:
        model = Chapter
        fields=('activityid','chapterid','chapersubject','chapercreated')

class ChapterarticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapterarticle
        fields=('activityid','chapterid','article')

class ChaptercommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chaptercomment 
        fields=('activityid','chapterid','commentcreated','comment')

class ChapterfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapterfile
        fields=('activityid','chapterid','filepath','filename')