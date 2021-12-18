# from _typeshed import FileDescriptorLike

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from activity.serializers import *
from connects.middleware import JWTValidation
from connects.utils import addTagName, addUserName
from managing.models import Activity


@api_view(['POST'])
def member(request, pk):
    if request.method == "POST":
        try:
            token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
            authed = token.decode_jwt()
            user_instance = User.objects.get(id=authed['user_id'])
        except:
            return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
        activity_instance = Activity.objects.get(pk=pk)
        if not ActivityParticipant.objects.filter(activity_id=activity_instance, user_id=user_instance):
            ActivityParticipant(activity_id=activity_instance, user_id=user_instance).save()
        return Response('Has Registered!', status=status.HTTP_200_OK)


@api_view(['POST'])
def out(request, pk):
    if request.method == "POST":
        try:
            token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
            authed = token.decode_jwt()
            user_instance = User.objects.get(id=authed['user_id'])
        except Exception as e:
            # print(e)
            return Response('auth_error', status=status.HTTP_400_BAD_REQUEST)
        activity_instance = Activity.objects.get(pk=pk)
        actiparti = ActivityParticipant.objects.get(activity_id=activity_instance, user_id=user_instance)
        actiparti.delete()
        return Response('Has Been Withdrawn', status=status.HTTP_200_OK)


@api_view(['GET'])
def ownActivity(request, pk):
    context = {'request': request}
    if request.method == "GET":
        user_instance = User.objects.get(id=pk)
        context = {'request': request}
        activities_instance = Activity.objects.filter(author=user_instance.email)
        serializer = ActivitySerializer(activities_instance, many=True, context=context)
        addTagName(serializer.data, Tag)
        addUserName(serializer.data, User)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def containedActivity(request):
    try:
        token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
        authed = token.decode_jwt()
        user_instance = User.objects.get(id=authed['user_id'])
    except Exception as e:
        # print(e)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)

    #start = time.time()
    acti_pt = ActivityParticipant.objects.filter(user_id=user_instance).only('activity_id')
    k = list()
    for i in acti_pt:
        kk = dict()
        kk['title'] = i.activity_id.title
        kk['description'] = i.activity_id.description
        kk['type'] = i.activity_id.type
        kk['activityid'] = i.activity_id.id
        k.append(kk)
    #print("time is", time.time() - start)
    return Response(k, status=status.HTTP_200_OK)


@api_view(['GET'])
def containedActivity_new(request):
    context = {'request': request}
    try:
        token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
        authed = token.decode_jwt()
        user_instance = User.objects.get(id=authed['user_id'])
    except Exception as e:
        # print(e)
        return Response('AUTHORIZATION ERROR', status=status.HTTP_400_BAD_REQUEST)
    # user_instance = User.objects.get(id=request.data['user_id'])

    #start = time.time()
    actiparti_instances = ActivityParticipant.objects.filter(user_id=user_instance).only('activity_id')
    activities_instances = [_act_pt.activity_id for _act_pt in actiparti_instances]
    serializer = ActivitySerializer(activities_instances, many=True, context=context)
    #print(serializer.data)
    #addTagName(serializer.data, Tag)
    #addUserName(serializer.data, User)

    #print("time is", time.time() - start)
    return Response(serializer.data, status=status.HTTP_200_OK)
