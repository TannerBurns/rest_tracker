from celery import shared_task

from .serializers import Rest_Tracker_Request_Serializer

@shared_task()
def rest_tracker_task(task_data):
    serializer = Rest_Tracker_Request_Serializer(data=task_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return serializer.errors

