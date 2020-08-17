from django.db import models

class Rest_Tracker_Status_Codes(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField(null=False)

    class Meta:
        db_table = 'rest_tracker_status_codes'
        app_label = 'rest_tracker'

class Rest_Tracker_Methods(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    method = models.CharField(null=False, max_length=16)

    class Meta:
        db_table = 'rest_tracker_methods'
        app_label = 'rest_tracker'

class Rest_Tracker_Schemes(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    scheme = models.TextField(null=False)

    class Meta:
        db_table = 'rest_tracker_schemes'
        app_label = 'rest_tracker'

class Rest_Tracker_Urls(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    host = models.TextField(null=False)
    path = models.TextField(null=False)
    raw = models.TextField(null=False)

    class Meta:
        db_table = 'rest_tracker_hosts'
        app_label = 'rest_tracker'

class Rest_Tracker_User_Agents(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(null=True)

    class Meta:
        db_table = 'rest_tracker_user_agents'
        app_label = 'rest_tracker'

class Rest_Tracker_Responses(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status_code = models.ForeignKey(Rest_Tracker_Status_Codes, on_delete=models.DO_NOTHING)
    content_size = models.IntegerField(default=0)

    class Meta:
        db_table = 'rest_tracker_response'
        app_label = 'rest_tracker'

class Rest_Tracker_Request(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    method = models.ForeignKey(Rest_Tracker_Methods, on_delete=models.DO_NOTHING)
    scheme = models.ForeignKey(Rest_Tracker_Schemes, on_delete=models.DO_NOTHING)
    url = models.ForeignKey(Rest_Tracker_Urls, on_delete=models.DO_NOTHING)
    user_agent = models.ForeignKey(Rest_Tracker_User_Agents, on_delete=models.DO_NOTHING)
    responses = models.ManyToManyField(Rest_Tracker_Responses)

    class Meta:
        db_table = 'rest_tracker_request'
        app_label = 'rest_tracker'
