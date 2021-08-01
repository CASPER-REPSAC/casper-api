from rest_framework import serializers
from .models import Activity, Chapter, Chapterarticle, Chaptercomment, Chapterfile

class ActivitySerializer():
    class Meta:
        model = Activity
        fields=('activityname','activitytype','acativityid')

class ChapterSerializer():
    class Meta:
        model = Chapter
        fields=('activityid','chapterid','chapersubject','chapercreated')

class ChapterarticleSerializer():
    class Meta:
        model = Chapterarticle
        fields=('activityid','chapterid','article')

class ChaptercommentSerializer():
    class Meta:
        model = Chaptercomment 
        fields=('activityid','chapterid','commentcreated','comment')

class ChapterfileSerializer():
    class Meta:
        model = Chapterfile
        fields=('activityid','chapterid','filepath','filename')