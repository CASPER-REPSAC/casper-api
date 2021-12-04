from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh_token'])
        data = {'access_token': str(refresh.access_token)}

        return data
'''
class RegistrationSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields=('email','username','password','first_name')
       extra_kwargs={'password':{'write_only':True}}
   def create(self,validated_data):
       password=validated_data.pop('password',None)
       instance=self.Meta.model(**validated_data)
       if password is not None:
           instance.set_password(password)
       instance.save()
       return instance


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('email','username','first_name')
        '''