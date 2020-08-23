from celery import shared_task

from . import ELASTIC_SESSION
from .models import REST_TRACKER_ES_MAPPING
from .serializers import Rest_Tracker_Request_Serializer

ES_INDEX = 'rest_tracker'

def write_to_es(data):
    es_content = {
        'created_at': data['created'],
        'scheme': data['scheme'],
        'method': data['method'],
        'url_host': data['url']['host'],
        'url_path': data['url']['path'],
        'url_raw': data['url']['raw'],
        'user_agent': data['user_agent'],
        'response_status_code': data['responses'][-1]['status_code'],
        'response_content_size': data['responses'][-1]['content_size']
    }
    return ELASTIC_SESSION.add_content(ES_INDEX, es_content)

@shared_task()
def rest_tracker_task(task_data):
    serializer = Rest_Tracker_Request_Serializer(data=task_data)
    if serializer.is_valid():
        serializer.save()
        if ELASTIC_SESSION.initialized and ELASTIC_SESSION.index_created:
            resp = write_to_es(serializer.data)
            if resp.status_code == 200:
                return serializer.data, resp.json()
            else:
                return serializer.data, resp.text
        return serializer.data
    else:
        return serializer.errors

@shared_task()
def initialize_es(host:str='elasticsearch', port:str='9200'):
    ELASTIC_SESSION.set_host(host)
    ELASTIC_SESSION.set_port(port)
    resp = ELASTIC_SESSION.create_index(ES_INDEX, REST_TRACKER_ES_MAPPING)
    if resp.status_code == 200:
        ELASTIC_SESSION.index_created = True
        return resp.json()
    else:
        return resp.text


