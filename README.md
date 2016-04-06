HotelAdmin
==========

Mock server which implements in Django the Standard SOAP Api.

_require (included in requirements.txt)：_
Django (1.8)
soaplib (2.0.0-beta2)
suds (0.4)


VirtualEnv:
==========
  It's possible running in a virtualenv:
  * In order to create a virtualenv you can follow the guidelines at: http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv/
  * After that you can install the requirements:
       * cd django
       * pip install -r requirements.txt
  * Then you can run the manage.py commands:
       * python manage.py runserver - or
       * python manage.py test
  * In order to access the different methods take in mind (there's should be running server in another terminal):
      $ python manage.py shell

        from suds.client import Client
        client = Client('http://localhost:8000/soap/hotel?wsdl')
        return_value = client.service.call("<method name=\"GetVersion\">"
                                           "<authentication name=\"matias\" systemkey=\"1234\">"
                                           "</authentication></method>")


Docker / Docker-Compose:
=======================
In order to simplify the setup process, a docker container was implemented. So in order to run it, you can download docker at
   * https://www.docker.com/
   * And then install docker-compose: https://docs.docker.com/compose/install/
  And follow the instructions there.

Running service using docker-compose (in project's root):
========================================================
* docker-compose build
* docker-compose up

Running the unit tests (in project's root):
==========================================
* docker-compose build
* docker-compose run web python manage.py test