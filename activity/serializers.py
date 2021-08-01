from rest_framework import serializers
from activity.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'type', 'author', 'createDate', 'introduce',
                  'startDate', 'endDate', 'currentState', 'viewerNum']

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Activity` instance, given the validated data.
    #     """
    #     return Activity.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Activity` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.type = validated_data.get("type", instance.type)
    #     instance.author = validated_data.get("author", instance.author)
    #     instance.createDate = validated_data.get("createDate", instance.createDate)
    #     instance.introduce = validated_data.get("introduce", instance.introduce)
    #     instance.startDate = validated_data.get("startDate", instance.startDate)
    #     instance.endDate = validated_data.get("endDate", instance.endDate)
    #     instance.currentState = validated_data.get("currentState", instance.currentState)
    #     instance.save()
    #     return instance

