# from _typeshed import FileDescriptorLike
import os, datetime, uuid, json, re
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, get_list_or_404
from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils.encoding import filepath_to_uri
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.files import File
from django.db.models import Q

from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser  # for file upload
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, serializers, status

from django.core.paginator import Paginator, EmptyPage
from django.conf import settings
from connects.middleware import JWTValidation
from connects.utils import addTagName, addUserName
from activity.serializers import TagSerializer
from activity.models import *
from accounts.models import *
from managing.serializers import *
from managing.models import Activity, Chapter, Chaptercomment, Chapterfile

from managing.utils import RandomFileName
import uuid, collections


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
        serializer = ActivityListSerializer(activities_instance, many=True, context=context)
        addTagName(serializer.data, Tag)
        addUserName(serializer.data, User)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def containedActivity(request):
    try:
        token = JWTValidation(request.META['HTTP_AUTHORIZATION'].split()[1])
        authed = token.decode_jwt()
        user_instance = User.objects.get(id=authed['user_id'])
        acti_pt = ActivityParticipant.objects.filter(user_id = user_instance).only('activity_id')
        
        k = list()
    
        for i in acti_pt:
            kk = dict()
            kk['title'] = i.activity_id.title
            kk['description'] = i.activity_id.description
            kk['type'] = i.activity_id.type
            kk['activityid'] = i.activity_id.id
            k.append(kk)
        return Response(k, status=status.HTTP_200_OK)


    except Exception as e:
        # print(e)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)


    #pass
    # context = {'request': request}
    # if request.method == "GET":
    #     user_instance = User.objects.get(id=pk)
    #     context = {'request': request}
    #     activities_instance = Activity.objects.filter(author=user_instance.email)
    #     serializer = ActivityListSerializer(activities_instance, many=True, context=context)
    #     addTagName(serializer.data, Tag)
    #     addUserName(serializer.data, User)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
