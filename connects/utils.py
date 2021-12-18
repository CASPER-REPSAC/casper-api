from rest_framework.utils.serializer_helpers import ReturnDict
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


def addUserName(response_data, User):
    user_list = User.objects.all()
    for d_idx, _object in enumerate(response_data):
        for o_idx, tag in enumerate(_object['participants']):
            response_data[d_idx]['participants'][o_idx]['user_name'] = str(user_list.get(pk=tag['user_id']))
    # return response_data # 리턴이 없어도 serializer.data 가 수정됨.


######end#####




