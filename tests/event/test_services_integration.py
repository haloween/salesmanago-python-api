import os
import random
import string
import logging
import requests
from unittest import skipIf
from unittest.mock import patch
from tests import utils as tests_utils
from .test_event_base import SalesManagoEventsServiceTestBase
from salesmanago_python_api.services.event import SalesManagoEventService
from salesmanago_python_api.data.event import SalesManagoEventData
from salesmanago_python_api.data.auth import SalesManagoAuthData


TEST_REAL_API = os.getenv('TEST_REAL_API', 'False')


class SalesManagoEventIntegrationTest(SalesManagoEventsServiceTestBase):

    client_logging = logging.getLogger('salesmanago_python_api.services.event')

    @patch.object(SalesManagoEventService, 'addContactExtEvent')
    def test_addContactExtEvent_action(self, mock_get) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = { 
            "eventId" : "21c252a6-6de0-436b-bae8-9d0142363266",
            "message" : [],
            "success" : True
        }

        rtn = self.clientClass.addContactExtEvent(self.eventClass)
        self.assertEqual(rtn.status_code, 200)
        self.assertIn('eventId', rtn.json())
        self.assertIn('success', rtn.json())


    @patch.object(SalesManagoEventService, 'batchAddContactExtEvent')
    def test_batchAddContactExtEvent_action(self, mock_get) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = { 
            "success" : True,
            "message" : [],
            "failedContacts": [],
            "createdAmount": 10,
            "failedAmount": 0
        }

        rtn = self.clientClass.batchAddContactExtEvent([self.eventClass])
        self.assertEqual(rtn.status_code, 200)
        self.assertIn('createdAmount', rtn.json())
        self.assertIn('success', rtn.json())

    '''
    @skipIf(TEST_REAL_API == 'False', 'Skipping tests that hit the real API server.')
    def test_real_insert_action(self) -> None:

        REAL_API_KEY = os.getenv('REAL_API_KEY', None)
        REAL_API_SECRET = os.getenv('REAL_API_SECRET', None)
        REAL_CLIENT_ID = os.getenv('REAL_CLIENT_ID', None)
        REAL_OWNER = os.getenv('REAL_OWNER', None)
        REAL_SERVER_DOMAIN = os.getenv('REAL_SERVER_DOMAIN', None)

        self.assertTrue(REAL_API_KEY)
        self.assertTrue(REAL_API_SECRET)
        self.assertTrue(REAL_CLIENT_ID)
        self.assertTrue(REAL_OWNER)
        self.assertTrue(REAL_SERVER_DOMAIN)

        REAL_VARS_CHECKLIST = [
            'REAL_API_KEY',
            'REAL_API_SECRET',
            'REAL_CLIENT_ID',
            'REAL_OWNER',
            'REAL_SERVER_DOMAIN'
        ]

        for a in REAL_VARS_CHECKLIST:
            varcheck = os.getenv(a, None)
            if not varcheck:
                self.skipTest('Required live test enviroment variables are not set')
        
        if REAL_API_KEY and REAL_API_SECRET and REAL_CLIENT_ID and REAL_OWNER and REAL_SERVER_DOMAIN:

            clientClass = SalesManagoEventService(
                apiKey=REAL_API_KEY, 
                clientId=REAL_CLIENT_ID, 
                apiSecret=REAL_API_SECRET, 
                serverDomain=REAL_SERVER_DOMAIN
            )

            clientDataClass = clientClass.ClientData
            clientData = clientDataClass(
                email='unittest@salesmanagopythonapi.pl',
                owner=REAL_OWNER
            )

            rtn = clientClass.insert(clientData)
            self.assertEqual(rtn.status_code, 200)
            self.assertIn('contactId', rtn.json())


    @skipIf(TEST_REAL_API == 'False', 'Skipping tests that hit the real API server.')
    def test_real_update_action(self) -> None:

        REAL_API_KEY = os.getenv('REAL_API_KEY', None)
        REAL_API_SECRET = os.getenv('REAL_API_SECRET', None)
        REAL_CLIENT_ID = os.getenv('REAL_CLIENT_ID', None)
        REAL_OWNER = os.getenv('REAL_OWNER', None)
        REAL_SERVER_DOMAIN = os.getenv('REAL_SERVER_DOMAIN', None)

        self.assertTrue(REAL_API_KEY)
        self.assertTrue(REAL_API_SECRET)
        self.assertTrue(REAL_CLIENT_ID)
        self.assertTrue(REAL_OWNER)
        self.assertTrue(REAL_SERVER_DOMAIN)

        REAL_VARS_CHECKLIST = [
            'REAL_API_KEY',
            'REAL_API_SECRET',
            'REAL_CLIENT_ID',
            'REAL_OWNER',
            'REAL_SERVER_DOMAIN'
        ]

        for a in REAL_VARS_CHECKLIST:
            varcheck = os.getenv(a, None)
            if not varcheck:
                self.skipTest('Required live test enviroment variables are not set')

        if REAL_API_KEY and REAL_API_SECRET and REAL_CLIENT_ID and REAL_OWNER and REAL_SERVER_DOMAIN:

            clientClass = SalesManagoEventService(
                apiKey=REAL_API_KEY, 
                clientId=REAL_CLIENT_ID, 
                apiSecret=REAL_API_SECRET, 
                serverDomain=REAL_SERVER_DOMAIN
            )

            clientDataClass = clientClass.ClientData
            clientData = clientDataClass(
                email='unittest@salesmanagopythonapi.pl',
                name='UPDATE NAME',
                owner=REAL_OWNER
            )

            rtn = clientClass.update(clientData)
            self.assertEqual(rtn.status_code, 200)
            RT_JSON = rtn.json()
            self.assertIn('contactId', RT_JSON)
            self.assertIn('success', RT_JSON)
            self.assertTrue(RT_JSON['success'])
    '''