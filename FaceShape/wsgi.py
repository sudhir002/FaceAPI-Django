import os
from facedetails.views import sio
import socketio
from socketio import Middleware
import eventlet
import eventlet.wsgi
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FaceShape.settings')


application = get_wsgi_application()
application = Middleware(sio, application)
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)