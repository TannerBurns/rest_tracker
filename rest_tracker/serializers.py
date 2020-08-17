from rest_framework import serializers

from .models import Rest_Tracker_Request, Rest_Tracker_Responses, Rest_Tracker_Methods, Rest_Tracker_Schemes, \
    Rest_Tracker_User_Agents, Rest_Tracker_Status_Codes, Rest_Tracker_Urls


class Rest_Tracker_Status_Codes_Serializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    status_code = serializers.IntegerField()

    class Meta:
        fields = ('id', 'created', 'status_code')
        read_only_fields = ('id', 'created')

    def to_representation(self, instance):
        return instance.status_code

class Rest_Tracker_Methods_Serializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    method = serializers.CharField()

    class Meta:
        fields = ('id', 'created', 'method')
        read_only_fields = ('id', 'created')

    def to_representation(self, instance):
        return instance.method

class Rest_Tracker_Schemes_Serializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    scheme = serializers.CharField()

    class Meta:
        fields = ('id', 'created', 'scheme')
        read_only_fields = ('id', 'created')

    def to_representation(self, instance):
        return instance.scheme

class Rest_Tracker_Urls_Serializer(serializers.Serializer):
    host = serializers.CharField()
    path = serializers.CharField()
    raw = serializers.CharField()

    class Meta:
        fields = ('host', 'path', 'raw')

class Rest_Tracker_User_Agents_Serializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    user_agent = serializers.CharField()

    class Meta:
        fields = ('id', 'created', 'user_agent')
        read_only_fields = ('id', 'created')

    def to_representation(self, instance):
        return instance.user_agent

class Rest_Tracker_Responses_Serializer(serializers.Serializer):
    created = serializers.DateTimeField(required=False)
    status_code = Rest_Tracker_Status_Codes_Serializer()
    content_size = serializers.IntegerField()

    class Meta:
        fields = ('created', 'status_code', 'content_size')
        read_only_fields = ('created', )

class Rest_Tracker_Request_Serializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    method = Rest_Tracker_Methods_Serializer()
    scheme = Rest_Tracker_Schemes_Serializer()
    url = Rest_Tracker_Urls_Serializer()
    user_agent = Rest_Tracker_User_Agents_Serializer()
    responses = Rest_Tracker_Responses_Serializer(many=True, required=False)

    class Meta:
        fields = ('id', 'created', 'method', 'scheme', 'url', 'user_agent', 'responses')
        read_only_fields = ('id', 'created')

    def create(self, validated_data):
        method_obj = Rest_Tracker_Methods.objects.get_or_create(**validated_data.pop('method'))[0]
        scheme_obj = Rest_Tracker_Schemes.objects.get_or_create(**validated_data.pop('scheme'))[0]
        url_obj = Rest_Tracker_Urls.objects.get_or_create(**validated_data.pop('url'))[0]
        user_agent_obj = Rest_Tracker_User_Agents.objects.get_or_create(**validated_data.pop('user_agent'))[0]
        responses = validated_data.pop('responses')
        req_obj = Rest_Tracker_Request.objects.get_or_create(method=method_obj, scheme=scheme_obj, url=url_obj,
                                                             user_agent=user_agent_obj)[0]
        for resp in responses:
            resp['status_code'] = Rest_Tracker_Status_Codes.objects.get_or_create(resp['status_code'])[0]
            resp_obj = Rest_Tracker_Responses.objects.create(**resp)
            req_obj.responses.add(resp_obj)
        req_obj.save()
        return req_obj
