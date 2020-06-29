import random
import string
import datetime
from unittest import TestCase
from tests import utils as tests_utils
from salesmanago_python_api.data.client import SalesManagoClientData


class SalesManagoTestsBase(TestCase):

    CLIENT_MAIL = 'client@test.pl'
    OWNER_MAIL = 'owner@test.pl'
    VALID_MAIL = 'valid@test.pl'
    INVALID_MAILS = ['xxxasd.pl', 'x@.pl', '@.pl', '.pl', '', 'username']

    CONTACT_FIELDS = [
        'state', 'fax', 'name', 'phone', 'company', 'address'
    ]

    ADDRESS_FIELDS = ['streetAddress', 'zipCode', 'city', 'country']

    VALID_STATES = ['CUSTOMER', 'PROSPECT', 'PARTNER', 'OTHER', 'UNKNOWN']

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

        self.rcd = self._rich_client_data()
        self.richClientClass = SalesManagoClientData(**self.rcd)

    def tearDown(self) -> None:
        pass