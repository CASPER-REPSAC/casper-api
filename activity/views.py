from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from activity.models import Activity
from activity.serializers import ActivitySerializer

@csrf_exempt
def activityList(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @csrf_exempt
    def activityDetail(request, pk):
        """
        Retrieve, update or delete a code snippet.
        """
        try:
            activity = Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = ActivitySerializer(activity)
            return JsonResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = ActivitySerializer(activity, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            activity.delete()
            return HttpResponse(status=204)