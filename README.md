# REST_Tracker

    Django app to easily track and store views request and responses

# Requirements

    python3.7+
    Celery backend for task management

# How To

Step 1: Pip install the rest-tracker library (this will install django, django-rest-framework, celery, redis, and psycopg2)
  
    pip3 install rest-tracker 
    
Step 2: Add the rest-tracker django app to the installed apps in settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'rest_framework',
    'rest_tracker'
]
```

Step 3: Add the tracker decorator to any Django View.

In this example, the /testing route is going to be tracked by rest-tracker
```python
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_tracker.decorators import tracker

# Create your views here.

class TestView(viewsets.GenericViewSet):

    @tracker
    @action(detail=False, methods=['get'])
    def testing(self, request):
        return Response({'testing': 'ok'}, status=200)
```

Step 4: Add the rest-tracker urls to start viewing the tracked data

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    ...
    path('', include('rest_tracker.urls'))
]
```

# Captured Data

The rest-track currently collects the following data per Request/Response

    Request: Method, Scheme, Host, Path, Raw URI, and User Agent
    Response: Status Code, Content Size

The following is an example of collected data from the test route

route /rest_tracker, method GET
```json
[
    {
        "id": 1,
        "created": "2020-08-17T00:44:02.050329Z",
        "method": "GET",
        "scheme": "http",
        "url": {
            "host": "127.0.0.1:8000",
            "path": "/test/testing",
            "raw": "http://127.0.0.1:8000/test/testing"
        },
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "responses": [
            {
                "created": "2020-08-17T00:51:23.059319Z",
                "status_code": 200,
                "content_size": 5952
            },
            {
                "created": "2020-08-17T00:51:35.809836Z",
                "status_code": 200,
                "content_size": 5956
            },
            {
                "created": "2020-08-17T01:15:36.772500Z",
                "status_code": 200,
                "content_size": 5956
            }
        ]
    },
    {
        "id": 2,
        "created": "2020-08-17T01:16:19.968399Z",
        "method": "POST",
        "scheme": "http",
        "url": {
            "host": "127.0.0.1:8000",
            "path": "/test/testing_post",
            "raw": "http://127.0.0.1:8000/test/testing_post"
        },
        "user_agent": "curl/7.54.0",
        "responses": [
            {
                "created": "2020-08-17T01:16:19.993153Z",
                "status_code": 200,
                "content_size": 16
            }
        ]
    }
]
```

The next example is the rest-tracker route for collecting counts based on these data points.

route /rest_tracker/counts, method GET
```json
{
    "methods": {
        "GET": 1,
        "POST": 1
    },
    "schemes": {
        "http": 2
    },
    "user_agents": {
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36": 1,
        "curl/7.54.0": 1
    },
    "hosts": {
        "127.0.0.1:8000": 2
    },
    "requests": 4
}
```

# Rest-Tracker Routes

    GET     /rest_tracker               Raw data from collected request and responses
    GET     /rest_tracker/counts        Counts based on collected request and responses
    GET     /rest_tracker/methods       Counts for methods collected from request
    GET     /rest_tracker/schemes       Counts for schemes collected from request
    GET     /rest_tracker/hosts         Counts for hosts collected from request
    GET     /rest_tracker/user_agents   Counts for user agents collected from request
    GET     /rest_tracker/requests      Overall count of requests that have been collected