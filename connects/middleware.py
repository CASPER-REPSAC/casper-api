import jwt
from rest_framework_simplejwt.tokens import Token, UntypedToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import (
    exceptions as err , 
    serializers
    )
from django.conf import settings

class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        return response

'''
class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        UntypedToken(attrs['token'])

        return {}

class TokenVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    serializer_class = TokenVerifySerializer
'''


class JWTValidation:

    def __init__(self, access_token):
        self.token = access_token

    def auth(self):
        t = self.decode_jwt()
        if not t :
            return False
        else :
            return True


    def decode_jwt(self):
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=["HS256"])
        except:
            payload = False
        
        if payload['pk'] is None:
            payload = False

        return payload