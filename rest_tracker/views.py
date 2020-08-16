from rest_framework import viewsets, mixins

from .models import Rest_Tracker_Request
from .serializers import Rest_Tracker_Request_Serializer


class Rest_Tracker_View(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Rest_Tracker_Request.objects.all().order_by('created')
    serializer_class = Rest_Tracker_Request_Serializer
