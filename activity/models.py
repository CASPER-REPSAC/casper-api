from django.db import models
from accounts.models import User
from django.contrib.auth import get_user_model

# Create your models here.
class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    type_CHOICES = (
        ('CTF', 'CTF'),
        ('Study', 'Study'),
        ('Project', 'Project'),
    )
    type = models.CharField(max_length=50, choices=type_CHOICES)
    author = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, db_column='author'),
    createDate = models.DateField(db_column='createDate')
    description = models.CharField(max_length=65)
    startDate = models.DateField(db_column='startDate')
    endDate = models.DateField(db_column='endDate')
    currentState_CHOICES = (
        (0, '0 : 예정'),
        (1, '1 : 진행'),
        (2, '2 : 종료'),
    )
    currentState = models.PositiveIntegerField(db_column='currentState', default=0,
                                               choices=currentState_CHOICES)
    viewerNum = models.PositiveIntegerField(db_column='viewerNum', default=0)

    class Meta:
        managed = True
        db_table = 'activity'
        ordering = ['-id']

    def __str__(self):
        return self.title




class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'tag'

    def __str__(self):
        return self.name


# Activity 와 Tag 관계 테이블
class ActivityTag(models.Model):
    activity_id = models.ForeignKey(Activity, related_name="tags", on_delete=models.CASCADE, db_column="activity_id")
    tag_id = models.ForeignKey(Tag, related_name="acti", on_delete=models.CASCADE, db_column='tag_id')

    class Meta:
        managed = True
        db_table = 'activity_tag'

    def __str__(self):
        return f"{self.activity_id} >-< {self.tag_id}"


# Activity 와 User 관계 테이블
class ActivityParticipant(models.Model):
    activity_id = models.ForeignKey(Activity, related_name="participants", on_delete=models.CASCADE,
                                    db_column="activity_id")
    user_id = models.ForeignKey('accounts.User', related_name='acti', on_delete=models.CASCADE, db_column='user_id')

    class Meta:
        managed = True
        db_table = 'activity_participant'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.TextField()
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)
