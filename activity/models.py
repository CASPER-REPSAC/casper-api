# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# Create your models here.
class Activity(models.Model):
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    createDate = models.DateField(db_column='createDate')  # Field name made lowercase.
    introduce = models.CharField(max_length=65)
    startDate = models.DateField(db_column='startDate')  # Field name made lowercase.
    endDate = models.DateField(db_column='endDate')  # Field name made lowercase.
    currentState = models.PositiveIntegerField(db_column='currentState', default=0)  # Field name made lowercase.
    viewerNum = models.PositiveIntegerField(db_column='viewerNum', default=0)  # Field name made lowercase.

    # owner = models.ForeignKey('auth.User', related_name='activities', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'activity'


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tag'

    def __str__(self):
        return self.name


# Activity 와 Tag 관계 테이블
class ActivityTag(models.Model):
    activity_id = models.ForeignKey(Activity, related_name="tags", on_delete=models.CASCADE,
                                    db_column="activity_id")
    tag_id = models.ForeignKey(Tag, related_name="acti", on_delete=models.CASCADE, db_column='tag_id')

    class Meta:
        managed = False
        db_table = 'activity_tag'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    # nickname = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


# Activity 와 User 관계 테이블
class ActivityParticipant(models.Model):
    activity_id = models.ForeignKey(Activity, related_name="participants", on_delete=models.CASCADE, db_column="activity_id")
    user_id = models.ForeignKey(AuthUser, related_name="acti", on_delete=models.CASCADE, db_column='user_id')

    # user_id = models.ForeignKey('auth.User', related_name='acti', on_delete=models.CASCADE,db_column='user_id')
    class Meta:
        managed = True
        db_table = 'activity_participant'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'
