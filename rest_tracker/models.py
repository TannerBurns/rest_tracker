from django.db import models


class Rest_Tracker_Response(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField(null=False)
    content_size = models.IntegerField(default=0)

    class Meta:
        db_table = 'rest_tracker_response'
        app_label = 'rest_tracker'

class Rest_Tracker_Request(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    method = models.CharField(null=False, max_length=16)
    scheme = models.TextField(null=False)
    host = models.TextField(null=False)
    path = models.TextField(null=False)
    raw = models.TextField(null=False)
    user_agent = models.TextField(null=True)
    responses = models.ManyToManyField(Rest_Tracker_Response)

    class Meta:
        db_table = 'rest_tracker_request'
        app_label = 'rest_tracker'
