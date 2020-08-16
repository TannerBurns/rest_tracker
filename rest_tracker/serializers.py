from rest_framework import serializers

from .models import Rest_Tracker_Request, Rest_Tracker_Response

class Rest_Tracker_Response_Serializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    status_code = serializers.IntegerField()
    content_size = serializers.IntegerField()

    class Meta:
        fields = ('id', 'created', 'status_code', 'content_size')
        read_only_fields = ('id', 'created')

class Rest_Tracker_Request_Serializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    method = serializers.CharField()
    scheme = serializers.CharField()
    host = serializers.CharField()
    path = serializers.CharField()
    raw = serializers.CharField()
    user_agent = serializers.CharField()
    responses = Rest_Tracker_Response_Serializer(many=True, required=False)

    class Meta:
        fields = ('id', 'created', 'method', 'scheme', 'host', 'path', 'raw', 'user_agent', 'responses')
        read_only_fields = ('id', 'created')

    def create(self, validated_data):
        responses = validated_data.pop('responses')
        req_obj = Rest_Tracker_Request.objects.get_or_create(**validated_data)[0]
        for resp in responses:
            resp_obj = Rest_Tracker_Response.objects.create(**resp)
            req_obj.responses.add(resp_obj)
        return req_obj