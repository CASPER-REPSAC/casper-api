from activity.models import Activity, ActivityTag, Tag
from activity.serializers import ActivitySerializer, ActivityTagSerializer, TagSerializer
# from rest_framework import generics
# from django.contrib.auth.models import User
# from activity.serializers import UserSerializer
from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# class ActivityList(generics.ListCreateAPIView):
#     queryset = Activity.objects.all()
#     serializer_class = ActivitySerializer
#
#
# class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Activity.objects.all()
#     serializer_class = ActivitySerializer
#
#
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         # 'users': reverse('user-list', request=request, format=format),
#         'activities': reverse('activity-list', request=request, format=format)
#     })


class ActivityViewSet(viewsets.ModelViewSet):
    """
    으앙
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)
    #
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """TagViewSet_"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ActivityTagViewSet(viewsets.ModelViewSet):
    """ActivityTagViewSet_"""
    queryset = ActivityTag.objects.all()
    serializer_class = ActivityTagSerializer
