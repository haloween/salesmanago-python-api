import random
from tests import utils as tests_utils


class EventTestDataMixin:
    CLIENT_MAIL = 'client@test.pl'
    OWNER_MAIL = 'owner@test.pl'
    VALID_MAIL = 'valid@test.pl'
    CONTACT_ID = '001e720f-b2ab-4203-a25f-b089557cf0da'
    EVENT_DATE = 1356180568153
    INVALID_MAILS = ['xxxasd.pl', 'x@.pl', '@.pl', '.pl', '', 'username']

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