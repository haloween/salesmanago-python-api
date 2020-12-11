import random
import string
import datetime
from unittest import TestCase
from tests import utils as tests_utils
from salesmanago_python_api.data.event import SalesManagoEventData
from salesmanago_python_api.data.client import SalesManagoClientData


class SalesManagoTestsBase(TestCase):

    CLIENT_MAIL = 'client@test.pl'
    OWNER_MAIL = 'owner@test.pl'
    VALID_MAIL = 'valid@test.pl'
    CONTACT_ID = '001e720f-b2ab-4203-a25f-b089557cf0da'
    EVENT_DATE = 1356180568153
    INVALID_MAILS = ['xxxasd.pl', 'x@.pl', '@.pl', '.pl', '', 'username']

    CONTACT_FIELDS = [
        'state', 'fax', 'name', 'phone', 'company', 'address'
    ]

    ADDRESS_FIELDS = ['streetAddress', 'zipCode', 'city', 'country']

    VALID_STATES = ['CUSTOMER', 'PROSPECT', 'PARTNER', 'OTHER', 'UNKNOWN']

    VALID_EVENTS = [
        'PURCHASE', 'CART', 'VISIT', 'PHONE_CALL', 'OTHER', 'RESERVATION', 'CANCELLED', 
        'ACTIVATION', 'MEETING', 'OFFER', 'DOWNLOAD', 'LOGIN', 'TRANSACTION', 'CANCELLATION', 
        'RETURN', 'SURVEY', 'APP_STATUS', 'APP_TYPE_WEB', 'APP_TYPE_MANUAL', 'APP_TYPE_RETENTION', 
        'APP_TYPE_UPSALE', 'LOAN_STATUS', 'LOAN_ORDER', 'FIRST_LOAN', 'REPEATED_LOAN'
    ]

    EXT_EVENT_FIELDS = [
        'description', 'products', 'location', 'value', 'externalId', 'shopDomain'
    ]

    def _min_event_data(self, fields=None):
        raw = {
            'email': self.CLIENT_MAIL,
            'owner': self.OWNER_MAIL,
            'contactId': self.CONTACT_ID,
            'eventDate': self.EVENT_DATE,
            'contactExtEventType': random.choice(self.VALID_EVENTS)
        }

        if fields:
            raw = {k:v for k,v in raw.items() if k in fields}

        return raw
    
    def _full_event_data(self, fields=None):
        raw = {
            'email': self.CLIENT_MAIL,
            'owner': self.OWNER_MAIL,
            'contactId': self.CONTACT_ID,
            'eventDate': self.EVENT_DATE,
            'contactExtEventType': random.choice(self.VALID_EVENTS),
            'forceOptIn': tests_utils.gen_true_false(),
            'description': tests_utils.gen_string(random.randint(4,120)),
            'products': tests_utils.gen_string(random.randint(4,120)),
            'location': tests_utils.gen_string(random.randint(4,120)),
            'value': random.randint(10,10000),
            'detail1': tests_utils.gen_string(random.randint(4,120)),
            'detail2': tests_utils.gen_string(random.randint(4,120)),
            'externalId': tests_utils.gen_string(random.randint(4,120)),
            'shopDomain': tests_utils.gen_string(random.randint(4,120))
        }

        if fields:
            raw = {k:v for k,v in raw.items() if k in fields}

        return raw

    def _rich_client_data(self, fields=None, no_address=False, no_contact=False):
        raw = {
            'name': tests_utils.gen_string(random.randint(4,120)),
            'email': self.CLIENT_MAIL,
            'owner': self.OWNER_MAIL,
            'phone': tests_utils.gen_string(random.randint(4,120)),
            'fax': tests_utils.gen_string(random.randint(4,120)),
            'company': tests_utils.gen_string(random.randint(4,120)),
            'birthday': datetime.date(1982,1,1),
            'newEmail': 'new@mail.pl',
            'address_streetAddress': tests_utils.gen_string(random.randint(4,120)),
            'address_zipCode': tests_utils.gen_string(random.randint(4,120)),
            'address_city': tests_utils.gen_string(random.randint(4,120)),
            'address_country': tests_utils.gen_string(random.randint(2,4)),
            'externalId': tests_utils.gen_string(random.randint(4,120)),
            'lang': 'PL',
            'state': random.choice(self.VALID_STATES),
            'forceOptOut': tests_utils.gen_true_false(),
            'forceOptIn': tests_utils.gen_true_false(),
            'forcePhoneOptOut': tests_utils.gen_true_false(),
            'forcePhoneOptIn': tests_utils.gen_true_false(),
            'useApiDoubleOptIn': tests_utils.gen_true_false(),
            'province': tests_utils.gen_string(random.randint(4,120))
        }

        if fields:
            raw = {k:v for k,v in raw.items() if k in fields}

        if no_address:
            raw = {k:v for k,v in raw.items() if 'address_' not in k}
        
        if no_contact:
            raw = {k:v for k,v in raw.items() if k not in self.CONTACT_FIELDS}

        return raw

    def setUp(self) -> None:
        self.clientClass = SalesManagoClientData(
            email=self.CLIENT_MAIL, owner=self.OWNER_MAIL
        )

        self.mcd = self._min_event_data()
        self.fcd = self._full_event_data()

        self.eventClass = SalesManagoEventData(**self.mcd)
        self.eventClassFull = SalesManagoEventData(**self.fcd)

        self.rcd = self._rich_client_data()
        self.richClientClass = SalesManagoClientData(**self.rcd)

    def tearDown(self) -> None:
        pass