#-*- coding: utf-8 -*-

import soaplib
from soaplib.core.server.wsgi import Application
from django.http import HttpResponse
import StringIO

from models import HotelAPIManager


class DumbStringIO(StringIO.StringIO):
    def read(self, n):
        return self.getvalue()


# Method to access SOAP Service from Django App
class DjangoSoapApp(Application):

    def __call__(self, request):
        django_response = HttpResponse()
        def start_response(status, headers):
            status, reason = status.split(' ', 1)
            django_response.status_code = int(status)
            for header, value in headers:
                django_response[header] = value

        environ = request.META.copy()
        environ['CONTENT_LENGTH'] = len(request.body)
        environ['wsgi.input'] = DumbStringIO(request.body)
        environ['wsgi.multithread'] = False

        try:
            response = super(DjangoSoapApp, self).__call__(environ, start_response)
        except Exception,e:
            error = str(e)
            raise Exception(u'Get the input date exception: '+ error)

        django_response.content = '\n'.join(response)
        return django_response

soap_application = soaplib.core.Application([HotelAPIManager], 'tns')
hotel = DjangoSoapApp(soap_application)
