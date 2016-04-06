"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import logging
from django.test.testcases import LiveServerTestCase
from suds.client import Client


class TestHotelAdminSOAP(LiveServerTestCase):

    def wsdl_url(self):
        return self.live_server_url + '/soap/hotel?wsdl'

    def test_get_version(self):
        """ Test GetVersion
        """
        client = Client(self.wsdl_url())
        # logging.basicConfig(level=logging.DEBUG)
        # Check a valid authentication
        return_value = client.service.call("<method name=\"GetVersion\">"
                                           "<authentication name=\"matias\" systemkey=\"1234\">"
                                           "</authentication></method>")
        self.assertEqual(return_value.response._status, 'ok')
        self.assertEqual(return_value.response.version._number, '2.0')
        self.assertEqual(return_value.response.server._product, 'name')
        # Check an invalid authentication
        return_value = client.service.call(
            "<method name=\"GetVersion\"><authentication name=\"matias\" systemkey=\"123dd4\">"
            "</authentication></method>")
        self.assertEqual(return_value.response._status, 'fail')

    def test_rooms_get_list(self):
        """ Test RoomsGetList
        """
        client = Client(self.wsdl_url())
        # Check a valid authentication
        # logging.basicConfig(level=logging.DEBUG)
        return_value = client.service.call("<method name=\"RoomsGetList\">"
                                           "<authentication name=\"matias\" systemkey=\"1234\">"
                                           "</authentication></method>")
        self.assertEqual(return_value.response._status, 'ok')
        # It should have 9 rooms
        self.assertEqual(len(return_value.response.rooms.room), 9)

    def test_rooms_lookup_list(self):
        """ Test RoomsLookupList
        """
        client = Client(self.wsdl_url())
        # Check a valid authentication
        # logging.basicConfig(level=logging.DEBUG)
        return_value = client.service.call("<method name=\"RoomsLookupList\" status=\"CheckedIn\" pattern=\"101\" "
                                           "field=\"Room\">"
                                           "<authentication name=\"matias\" systemkey=\"1234\">"
                                           "</authentication></method>")
        self.assertEqual(return_value.response._status, 'ok')
        self.assertEqual(len(return_value.response.rooms), 1)
        self.assertEqual(return_value.response.rooms.room._id, '1')

    def test_invoice_to_room(self):
        """
        Test InvoiceToRoom
        """
        client = Client(self.wsdl_url())
        # logging.basicConfig(level=logging.DEBUG)
        return_value = client.service.call(
            "<method name=\"InvoiceToRoom\"><authentication name=\"matias\" systemkey=\"1234\">"
            "</authentication><roomid>1</roomid></method>")
        self.assertEqual(return_value.response._status, 'ok')
        # Check an invalid roomid
        return_value = client.service.call(
            "<method name=\"InvoiceToRoom\"><authentication name=\"matias\" systemkey=\"1234\">"
            "</authentication><roomid>300</roomid></method>")
        self.assertEqual(return_value.response._status, 'fail')