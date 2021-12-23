from django.db import models
from django.contrib.auth import get_user_model
from activity.models import *
import connects.settings as sett

User = get_user_model()

class Chapter(models.Model):
    activityid = models.ForeignKey(Activity, related_name='chapterid',db_column='activityid', on_delete=models.CASCADE)#related_name='chapterid', on_delete=models.CASCADE)
    chapterid = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=16)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    article = models.CharField(max_length=500)
    filepath = models.CharField(max_length=32, blank=True, null=True)
    fileid = models.IntegerField(blank=True, null=True)
    last = models.IntegerField(default=0, blank=True,null=True)
    next = models.IntegerField(default=0, blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'chapter'

    def __str__(self):
        return self.subject


class Chaptercomment(models.Model):
    commentpk = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=100)
    activityid = models.ForeignKey(Activity, related_name='commentpk', db_column='activityid', on_delete=models.CASCADE)
    chapterid = models.ForeignKey(Chapter, related_name='commentpk', db_column='chapterid', on_delete=models.CASCADE)
    createtime = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, related_name='commenter', db_column='writer', on_delete=models.CASCADE)

    class Meta:
        managed = True
        ordering = ['createtime']
        db_table = 'chaptercomment'


class Chapterfile(models.Model):
    filepk = models.AutoField(primary_key=True)
    activityid = models.ForeignKey(Activity, db_column='activityid', on_delete=models.CASCADE)
    chapterid = models.ForeignKey(Chapter, db_column='chapterid', on_delete=models.CASCADE)
    filepath = models.CharField(max_length=64)
    filename = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    fileext = models.CharField(max_length=5)
    file = models.FileField(upload_to=sett.MEDIA_URL, null=False)
    def __str__(self):
        return self.filename

    class Meta:
        managed = True
        ordering = ['chapterid']
        db_table = 'chapterfile'
