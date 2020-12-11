import random
from tests import utils as tests_utils
from .test_data_base import SalesManagoTestsBase


class SalesManagoClientDataFeatureTest(SalesManagoTestsBase):

    def test_requestDict_for_minimal(self):
        AGAINST = {
            'email': self.CLIENT_MAIL,
            'owner': self.OWNER_MAIL,
            'contactId': self.CONTACT_ID,
            'contactEvent': {
                'date': self.EVENT_DATE,
                'contactExtEventType': self.mcd['contactExtEventType']
            }
        }

        TEST_DICT = self.eventClass.requestDict()

        self.assertEqual(AGAINST, TEST_DICT)

        for ext_field in self.EXT_EVENT_FIELDS:
            self.assertNotIn(ext_field, TEST_DICT)
            self.assertNotIn(ext_field, TEST_DICT['contactEvent'])

    def test_requestDict_for_full(self):

        AGAINST = {
            'email': self.CLIENT_MAIL,
            'owner': self.OWNER_MAIL,
            'contactId': self.CONTACT_ID,
            'forceOptIn': self.fcd['forceOptIn'],
            'contactEvent': {
                'date': self.EVENT_DATE,
                'contactExtEventType': self.fcd['contactExtEventType'],
                'products': self.fcd['products'],
                'location': self.fcd['location'],
                'value': self.fcd['value'],
                'detail1': self.fcd['detail1'],
                'detail2': self.fcd['detail2'],
                'description': self.fcd['description'],
                'externalId': self.fcd['externalId'],
                'shopDomain': self.fcd['shopDomain']
            }
        }

        TEST_DICT = self.eventClassFull.requestDict()
        self.assertEqual(AGAINST, TEST_DICT)
