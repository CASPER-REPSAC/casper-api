from rest_framework import serializers
from activity.models import Activity, ActivityTag, Tag


# from django.contrib.auth.models import User


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = ['url', 'id', 'title', 'type', 'author', 'createDate', 'introduce',
                  'startDate', 'endDate', 'currentState', 'viewerNum']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'id', 'name']


class ActivityTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityTag
        fields = ['url', 'activity', 'tag']

# class UserSerializer(serializers.ModelSerializer):
#     activities = serializers.PrimaryKeyRelatedField(many=True, queryset=Activity.objects.all())
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'activities']
