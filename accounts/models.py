from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, first_name,last_name, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        #print(**extra_fields)
        return user

    def create_superuser(self, email, first_name,last_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, first_name,last_name, password, **extra_fields)


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = None
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id','first_name','last_name']

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        db_table = 'accounts_user'
        managed = True
        
    def __str__(self):
        return self.email

class UserReturn(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    class Meta:
        db_table = 'accounts_user'
        managed = False

#socialaccount_socialaccount
class SocialUser(models.Model):
    id = models.AutoField(primary_key=True)
    extra_data = models.TextField()
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
