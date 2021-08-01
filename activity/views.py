from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from activity.models import Activity
from activity.serializers import ActivitySerializer


@api_view(['GET', 'POST'])
def activityList(request, format=None):
    """
    List all activities, or create a new activity.
    """
    if request.method == 'GET':
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def activityDetail(request, pk, format=None):
    """
    Retrieve, update or delete a activity.
    """
    try:
        activity = Activity.objects.get(pk=pk)
    except Activity.DoesNotExist:
        return HttpResponse(status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        activity.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
