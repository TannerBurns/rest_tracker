from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Rest_Tracker_Request, Rest_Tracker_Methods, Rest_Tracker_Schemes, Rest_Tracker_User_Agents, \
    Rest_Tracker_Urls
from .serializers import Rest_Tracker_Request_Serializer



class Rest_Tracker_View(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Rest_Tracker_Request.objects.all().order_by('created')
    serializer_class = Rest_Tracker_Request_Serializer

    def count_methods(self):
        value_list = Rest_Tracker_Methods.objects.values_list('method', flat=True).distinct()
        base = {val: 0 for val in value_list}
        for val in value_list:
            for object in Rest_Tracker_Request.objects.filter(method__method=val):
                base[val] += object.responses.count()
        return base

    def count_schemes(self):
        value_list = Rest_Tracker_Schemes.objects.values_list('scheme', flat=True).distinct()
        base = {val: 0 for val in value_list}
        for val in value_list:
            for object in Rest_Tracker_Request.objects.filter(scheme__scheme=val):
                base[val] += object.responses.count()
        return base

    def count_user_agents(self):
        value_list = Rest_Tracker_User_Agents.objects.values_list('user_agent', flat=True).distinct()
        base = {val: 0 for val in value_list}
        for val in value_list:
            for object in Rest_Tracker_Request.objects.filter(user_agent__user_agent=val):
                base[val] += object.responses.count()
        return base

    def count_hosts(self):
        value_list = Rest_Tracker_Urls.objects.values_list('host', flat=True).distinct()
        base = {val: 0 for val in value_list}
        for val in value_list:
            for object in Rest_Tracker_Request.objects.filter(url__host=val):
                base[val] += object.responses.count()
        return base

    def count_requests(self):
        total = 0
        for objects in Rest_Tracker_Request.objects.all():
            total += objects.responses.all().count()
        return {'requests': total}


    @action(detail=False, methods=['get'])
    def methods(self, _):
        return Response(self.count_methods(), status=200)

    @action(detail=False, methods=['get'])
    def schemes(self, _):
        return Response(self.count_schemes(), status=200)

    @action(detail=False, methods=['get'])
    def user_agents(self, _):
        return Response(self.count_user_agents(), status=200)

    @action(detail=False, methods=['get'])
    def hosts(self, _):
        return Response(self.count_hosts(), status=200)

    @action(detail=False, methods=['get'])
    def requests(self, _):
        return Response(self.count_requests(), status=200)

    @action(detail=False, methods=['get'])
    def counts(self, _):
        content = {
            'methods': self.count_methods(), 'schemes': self.count_schemes(), 'user_agents': self.count_user_agents(),
            'hosts': self.count_hosts(), **self.count_requests()
        }
        return Response(content, status=200)



