from django.core.handlers.wsgi import WSGIHandler
from django.dispatch import Signal
from django.http import parse_cookie

__author__ = 'Maxaon'

demo_request = Signal()


class DemoHandler(WSGIHandler):
    def __call__(self, environ, start_response):
        cookies = environ.get('HTTP_COOKIE')
        if cookies and 'demo_db' in cookies:
            parsed_cookies = parse_cookie(cookies)
            demo_request.send(self.__class__, cookie=parsed_cookies['demo_db'])

        return super(DemoHandler, self).__call__(environ, start_response)