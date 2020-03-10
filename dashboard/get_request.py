# thanks to: https://stackoverflow.com/a/54083141
import threading
from typing import Union
from django.http import HttpRequest
from django.middleware.http import MiddlewareMixin

request_local = threading.local()


def get_request() -> Union[HttpRequest, None]:
    return getattr(request_local, 'request', None)


class RequestMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_local.request = request
        return self.get_response(request)

    def process_exception(self, request, exception):
        request_local.request = None

    def process_template_response(self, request, response):
        request_local.request = None
        return response
