from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict
from connects.middleware import JWTValidation
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from accounts.models import SocialUser
import json

def addTagName(response_data, Tag):
    tag_list = Tag.objects.all()
    # post 로 생성할 때는 response_data 의 데이터 타입이 다름.
    # get 으로 불러올 떄는 ReturnDict 가 list 로 묶여있어서 ReturnList 이 되나봄.
    # 그래서 아래와 같이 따로 처리 해줌.
    if type(response_data) == ReturnDict:
        for o_idx, tag_id in enumerate(response_data['tags']):
            response_data['tags'][o_idx]['tag_name'] = str(tag_list.get(pk=tag_id['tag_id']))
    else:
        for d_idx, _object in enumerate(response_data):
            for o_idx, tag in enumerate(_object['tags']):
                response_data[d_idx]['tags'][o_idx]['tag_name'] = str(tag_list.get(pk=tag['tag_id']))
    # return response_data # 리턴이 없어도 serializer.data 가 수정됨.


# 새로운 버전의 addUserName 함수
def addUserName(response_data, User):
    user_list = User.objects.all()
    social_userlist = SocialUser.objects.all()

    if type(response_data) == ReturnDict:
        for o_idx, user in enumerate(response_data['participants']):
            #_user = user_list.get(pk=user['user_id'])
            _social = social_userlist.get(pk=user['user_id'])
            #print(json.loads(str(_social.extra_data)))
            _json = json.loads(str(_social.extra_data))
            _json.pop('verified_email')
            _json.pop('id')
            _json.pop('locale')

            ##tmp
            response_data['participants'][o_idx]['user_name'] = _json["name"]

            ## Need to Change
            #response_data['participants'][o_idx]['user_name'] = str(_user.email)
            #response_data['participants'][o_idx]['first_name'] = str(_user.first_name)
            #response_data['participants'][o_idx]['last_name'] = str(_user.last_name)

            #response_data['participants'][o_idx]['picture'] = _json["picture"]
            #response_data['participants'][o_idx]['user_name'] = _json["email"]
            #response_data['participants'][o_idx]['first_name'] = _json["given_name"]
            #response_data['participants'][o_idx]['last_name'] = _json["name"]
    else:
        for d_idx, _object in enumerate(response_data):
            for o_idx, user in enumerate(_object['participants']):
                #_user = user_list.get(pk=user['user_id'])
                _social = social_userlist.get(pk=user['user_id'])
                _json = json.loads(str(_social.extra_data))
                _json.pop('verified_email')
                _json.pop('id')
                _json.pop('locale')
                
                response_data[d_idx]['participants'][o_idx]['profile'] = _json

                ##tmp
                response_data[d_idx]['participants'][o_idx]['user_name'] = _json["name"]


                ## Need to Change
                #response_data[d_idx]['participants'][o_idx]['user_name'] = str(_user.email)
                #response_data[d_idx]['participants'][o_idx]['first_name'] = str(_user.first_name)
                #response_data[d_idx]['participants'][o_idx]['last_name'] = str(_user.last_name)
                
                #response_data[d_idx]['participants'][o_idx]['picture'] = _json["picture"]
                #response_data[d_idx]['participants'][o_idx]['user_name'] = _json["email"]
                #response_data[d_idx]['participants'][o_idx]['first_name'] = _json["given_name"]
                #response_data[d_idx]['participants'][o_idx]['last_name'] = _json["name"]
  



def USER_AUTHORIZAION(request):
    User = get_user_model()
    try:
        token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
        authed = token.decode_jwt()
        return User.objects.get(id=authed['user_id'])
    except:
        return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
