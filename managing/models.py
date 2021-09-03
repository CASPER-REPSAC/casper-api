from django.db import models

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    type_CHOICES = (
        ('CTF', 'CTF'),
        ('Study', 'Study'),
        ('Project', 'Project'),
    )
    type = models.CharField(max_length=50, choices=type_CHOICES)
    author = models.CharField(max_length=50)
    # owner = models.ForeignKey('auth.User', related_name='activities', on_delete=models.CASCADE)
    # author 를 owner 로 교체해야할 때가 올 것임..
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
        managed = False
        db_table = 'activity'

    def __str__(self):
        return self.title

class Chapter(models.Model):
    activityid = models.ForeignKey(Activity, related_name='chapterid',db_column='activityid', on_delete=models.CASCADE)#related_name='chapterid', on_delete=models.CASCADE)
    chapterid = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=16)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    article = models.CharField(max_length=500)
    filepath = models.CharField(max_length=32, blank=True, null=True)
    filesize = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chapter'

class Chaptercomment(models.Model):
    commentpk = models.AutoField(primary_key=True)
    activityid = models.IntegerField()
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='chapterid')
    comment = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'chaptercomment'


class Chapterfile(models.Model):
    filepk = models.AutoField(primary_key=True)
    activityid = models.IntegerField()
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='chapterid')
    filepath = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'chapterfile'


###


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

    class Meta:
        managed = False
        db_table = 'auth_user'


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