from soaplib.core.service import soap
from soaplib.core.service import DefinitionBase
from soaplib.core.model.primitive import Any
import xml.etree.ElementTree as ET
import random
import string


def random_code(size=6, chars=string.ascii_uppercase + string.digits):
    """random_code: Creates a random alpha-numeric code of size defined"""
    return ''.join(random.choice(chars) for _ in range(size))


def random_string(size=20, chars=string.ascii_uppercase):
    """random_string: Creates a random alphabetic string of size defined"""
    return ''.join(random.choice(chars) for _ in range(size))


def random_phone(size=10, chars=string.digits):
    """random_phone: Creates a random numeric string of size defined"""
    return ''.join(random.choice(chars) for _ in range(size))

# Possible field searching in rooms
POSSIBLE_FIELD_VALUES = ['Id', 'Full', 'Room', 'Name', 'Phone', 'Address', 'Email']

# Random generation of 100 rooms
rooms_list = [{'id': str(i), 'name': str(i), 'room': str(100+i), 'guestname': random_string(40),
               'resid': random_code(), 'phone': random_phone()}
              for i in xrange(1, 10)]


class HotelAPIManager(DefinitionBase):

    def find_rooms(self, status, pattern, field):
        # TODO: Status only 'CheckedIn'. In the future: 'All' and 'Available'
        # TODO: Full pattern for later
        if field in POSSIBLE_FIELD_VALUES and field != 'Full':
            field = field.lower()
            filtered_list = filter(lambda room: room[field] == pattern, rooms_list)
            return filtered_list
        # Else return all the list
        return rooms_list

    def check_auth(self, auth):
        return auth.get('systemkey') == '1234'

    @soap(Any, _returns=Any)
    def call(self, method):
        if method.tag == 'method':
            if 'name' in method.attrib:
                method_name = method.attrib['name']
                # Authentication validation
                auth = method[0]
                if auth.tag == 'authentication':
                    if not self.check_auth(auth.attrib):
                        return "<response status=\"fail\"><err code=\"100\" msg=\"Invalid system key\"/></response>"
                # Check which is the method
                response_ok = ET.Element("response", status='ok')
                response_fail = ET.Element("response", status='fail')
                if method_name == 'GetVersion':
                    response_ok.append(ET.Element("version", number='2.0'))
                    response_ok.append(ET.Element("server", product='name'))
                # The method for RoomsGetList and RoomsLookupList is almost the same but the parameters in find_rooms
                if method_name == 'RoomsGetList' or method_name == 'RoomsLookupList':
                    status = method.attrib.get('status', 'CheckedIn')
                    pattern = method.attrib.get('pattern')
                    field = method.attrib.get('field')
                    # TODO: status === 'CheckedIn' or 'All' or 'Available'
                    rooms = ET.Element('rooms')
                    room_list_found = self.find_rooms(status, pattern, field)
                    for room in room_list_found:
                        room_xml = ET.Element('room')
                        for key, attribute in room.iteritems():
                            room_xml.set(key, attribute)
                        rooms.append(room_xml)
                    response_ok.append(rooms)
                if method_name == 'InvoiceToRoom':
                    # Validation
                    for entity in method:
                        # Check room existance
                        if entity.tag == 'roomid':
                            if len(self.find_rooms('CheckedIn', entity.text, 'Id')) != 1:
                                response_fail.append(ET.Element("err", {'code': '300', 'msg': 'Invalid room'}))
                                return ET.tostring(response_fail)
                        # resid should be filled
                        if entity.tag == 'resid':
                            if len(entity.text) == 0:
                                response_fail.append(ET.Element("err", {'code': '301', 'msg': 'ResId is mandatory'}))
                                return ET.tostring(response_fail)
                return ET.tostring(response_ok)