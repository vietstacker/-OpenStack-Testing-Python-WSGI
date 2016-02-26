"""The Python libraries used"""

from eventlet import greenthread
from eventlet import wsgi
from eventlet import listen

import webob
from webob import Response
from webob.dec import wsgify


"""Let's create a wsgi application"""


class Application(object):
    """Base WSGI application wrapper. Subclasses need to implement __call__."""
    def __call__(self, req):
        raise NotImplementedError(_('You must implement __call__'))


class Simple_app(Application):
    @wsgify(RequestClass=Request)
    def __call__(self, request):
        response_headers = [('Content-Type', 'text/plain')]
        if request.environ['REQUEST_METHOD'] == "GET":
            status = "200 OK"
            body = """ From VietStack: Wellcome the 8th Meetup of VietOpenStack \n"""
        
        return Response(status=status, headers=response_headers, body=body)


"""Here is the middleware code"""


class Middleware(object):
    """ This class will act as a middleware that receives a request
    then passes the request on to the wsgi application.
    """
    def __init__(self, app):
        self.app = app

    @wsgify
    def __call__(self, req):
        try:
            resp = req.get_response(self.app)
        except Exception:
            pass
        return resp


"""Finally, the wsgi server"""

class Server(object):
    def __init__(self, response):
        self.response = response
        
    def create_worker_thread(self):
        listener_socket = self.create_listener_socket()
        return greenthread.spawn(wsgi.server, listener_socket, self.response)
    
    def create_listener_socket(self):
        return listen(('localhost', 8080))

    def start(self):
        self.worker_thread = self.create_worker_thread()
        self.worker_thread.wait()


"""And now is the recipe""" 

simple_app = Simple_app()

''' Middleware returns response'''
middle_ware = Middleware(simple_app)

''' Server gets the response from middleware '''
server = Server(middle_ware)
server.start()
