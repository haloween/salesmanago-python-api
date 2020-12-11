import datetime
from unittest import TestCase
from .test_event_base import SalesManagoEventsTestsBase
from tests.utils import gen_list_of_strings, gen_dict
from salesmanago_python_api.data.event import SalesManagoEventData


class SalesManagoEventDataUnitTest(SalesManagoEventsTestsBase):

    def test_create_minimal_event_with_email(self):
        _min_event_data = self._min_event_data(fields=['owner', 'email', 'eventDate', 'contactExtEventType'])
        clientClass = SalesManagoEventData(**_min_event_data)
        self.assertEqual(clientClass.owner, _min_event_data['owner'])
        self.assertEqual(clientClass.eventDate, _min_event_data['eventDate'])
        self.assertEqual(clientClass.email, _min_event_data['email'])

    def test_create_minimal_event_with_contactId(self):
        _min_event_data = self._min_event_data(fields=['owner', 'contactId', 'eventDate', 'contactExtEventType'])
        clientClass = SalesManagoEventData(**_min_event_data)
        self.assertEqual(clientClass.owner, _min_event_data['owner'])
        self.assertEqual(clientClass.eventDate, _min_event_data['eventDate'])
        self.assertEqual(clientClass.contactId, _min_event_data['contactId'])
    
    def test_create_minimal_event_wo_owner(self):
        _min_event_data = self._min_event_data(fields=['email', 'eventDate', 'contactExtEventType'])
        with self.assertRaises(ValueError):
            SalesManagoEventData(**_min_event_data)

    def test_create_minimal_event_wo_mail_and_wo_contact(self):
        _min_event_data = self._min_event_data(fields=['owner','eventDate', 'contactExtEventType'])
        with self.assertRaises(ValueError):
            SalesManagoEventData(**_min_event_data)

    def test_create_minimal_event_wo_eventDate(self):
        _min_event_data = self._min_event_data(fields=['owner','contactId', 'contactExtEventType'])
        with self.assertRaises(ValueError):
            SalesManagoEventData(**_min_event_data)
    
    def test_create_minimal_event_wo_contactExtEventType(self):
        _min_event_data = self._min_event_data(fields=['owner','eventDate','contactId'])
        with self.assertRaises(ValueError):
            SalesManagoEventData(**_min_event_data)

    def test_contactExtEventType_values_on_creation(self):
        with self.assertRaises(ValueError):
            _min_event_data = self._min_event_data()
            _min_event_data['contactExtEventType'] = 'ASDASDA'
            cd = SalesManagoEventData(**_min_event_data)

    def test_contactExtEventType_values_on_change(self):
        with self.assertRaises(ValueError):
            _min_event_data = self._min_event_data()
            cd = SalesManagoEventData(**_min_event_data)
            cd.contactExtEventType = 'ASDASDA'
    
    def test_contactExtEventType_allowed_values(self):
        _min_event_data = self._min_event_data()
        for eventType in self.VALID_EVENTS:

            _min_event_data['contactExtEventType'] = eventType

            clientClass = SalesManagoEventData(**_min_event_data)
            self.assertEqual(clientClass.contactExtEventType, eventType)

    def test_event_email_validated_on_create(self):
        _min_event_data = self._min_event_data()

        with self.assertRaises(ValueError):
            for invalid_email in self.INVALID_MAILS:
                _min_event_data['email'] = invalid_email
                SalesManagoEventData(**_min_event_data)

    def test_email_validated_on_change(self):
        _min_event_data = self._min_event_data()

        with self.assertRaises(ValueError):
            for invalid_email in self.INVALID_MAILS:
                cd = SalesManagoEventData(**_min_event_data)
                cd.email = invalid_email

    def test_owner_validated_on_create(self):
        _min_event_data = self._min_event_data()

        with self.assertRaises(ValueError):
            for invalid_email in self.INVALID_MAILS:
                _min_event_data['owner'] = invalid_email
                SalesManagoEventData(**_min_event_data)
    
    def test_owner_validated_on_change(self):
        _min_event_data = self._min_event_data()

        with self.assertRaises(ValueError):
            for invalid_email in self.INVALID_MAILS:
                cd = SalesManagoEventData(**_min_event_data)
                cd.owner = invalid_email

    def test_create_rich_event_with_invalid_eventDate_type(self):
        _min_event_data = self._min_event_data()
        _min_event_data['eventDate'] = '20200101'

        with self.assertRaises(TypeError):
            SalesManagoEventData(**_min_event_data)

        _min_event_data['eventDate'] = datetime.date.today()

        with self.assertRaises(TypeError):
            SalesManagoEventData(**_min_event_data)
    
    def test_change_eventDate_to_invalid_type(self):
        _min_event_data = self._min_event_data()

        with self.assertRaises(TypeError):
            cd = SalesManagoEventData(**_min_event_data)
            cd.eventDate = datetime.date.today()
            cd.eventDate = '20200101'
    
    def test_create_full_event(self):
        _full_event_data = self._full_event_data()
        clientClass = SalesManagoEventData(**_full_event_data)
