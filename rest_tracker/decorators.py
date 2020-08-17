from rest_framework.request import Request
from typing import Callable
from functools import update_wrapper
from threading import Thread

from .tasks import rest_tracker_task

def start_task(request, response):
    response.accepted_renderer, response.accepted_media_type = request.accepted_renderer, request.accepted_media_type
    response.renderer_context = request.parser_context
    response.render()
    task_data = {
        'method': {'method':request.method},
        'scheme': {'scheme':request.scheme},
        'url': {
            'host':request.get_host(),
            'path': request.path,
            'raw': request.get_raw_uri()
        },
        'user_agent': {'user_agent': request.headers.get('User-Agent', 'UNKNOWN')},
        'responses': [{
            'status_code': {'status_code':response.status_code}, 'content_size': len(response.content)
        }]
    }
    rest_tracker_task.delay(task_data)


class tracker(object):
    def __init__(self, function: Callable):
        """initialize aiobulk
        the function being decorated will receive a new attribute for the bulk call
        :param function: function being decorated
        """
        self.__self__ = None
        self.__bound__ = function
        update_wrapper(self, function)

    def __call__(self, *args: tuple, **kwargs: dict):
        """call base function"""
        if self.__self__ is not None:
            args = (self.__self__,) + args
        response = self.__bound__(*args, **kwargs)
        for a in args:
            if isinstance(a, Request):
                Thread(target=start_task, args=(a, response)).start()
                break
        return response

    def __get__(self, instance, _):
        """update self if instance is found
        :param instance: cls instance
        :return: return self with instance
        """
        if instance is None:
            return self
        else:
            self.__self__ = instance
            return self