import os
import random
import string
import logging
import requests
from unittest import skipIf
from unittest.mock import patch
from tests import utils as tests_utils
from .test_services_base import SalesManagoClientTestBase
from salesmanago_python_api.services.client import SalesManagoClientService
from salesmanago_python_api.data.client import SalesManagoClientData
from salesmanago_python_api.data.auth import SalesManagoAuthData


TEST_REAL_API = os.getenv('TEST_REAL_API', 'False')


class SalesManagoClientIntegrationTest(SalesManagoClientTestBase):

    client_logging = logging.getLogger('salesmanago_python_api.services.client')

    @patch.object(SalesManagoClientService, 'insert')
    def test_insert_action(self, mock_get) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = { 
            "contactId" : "21c252a6-6de0-436b-bae8-9d0142363266",
            "message" : [],
            "success" : True,
            "externalId": None
        }

        rtn = self.clientClass.insert(self.clientDataMock)
        self.assertEqual(rtn.status_code, 200)
        self.assertIn('contactId', rtn.json())


    @patch.object(SalesManagoClientService, 'update')
    def test_update_action(self, mock_get) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = { 
            "contactId" : "21c252a6-6de0-436b-bae8-9d0142363266",
            "message" : [],
            "success" : True,
            "externalId": None
        }

        rtn = self.clientClass.update(self.clientDataMock)
        self.assertEqual(rtn.status_code, 200)
        self.assertIn('contactId', rtn.json())
    
    @patch.object(SalesManagoClientService, 'upsert')
    def test_upsert_action(self, mock_get) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = { 
            "contactId" : "21c252a6-6de0-436b-bae8-9d0142363266",
            "message" : [],
            "success" : True,
            "externalId": None
        }

        rtn = self.clientClass.upsert(self.clientDataMock)
        self.assertEqual(rtn.status_code, 200)
        self.assertIn('success', rtn.json())


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

            clientClass = SalesManagoClientService(
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

            clientClass = SalesManagoClientService(
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

    @skipIf(TEST_REAL_API == 'False', 'Skipping tests that hit the real API server.')
    def test_real_upsert_action(self) -> None:

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

            clientClass = SalesManagoClientService(
                apiKey=REAL_API_KEY, 
                clientId=REAL_CLIENT_ID, 
                apiSecret=REAL_API_SECRET, 
                serverDomain=REAL_SERVER_DOMAIN
            )

            clientDataClass = clientClass.ClientData
            clientData = clientDataClass(
                email='unittest@salesmanagopythonapi.pl',
                name='UPDATE NAME',
                tags=['upsert'],
                owner=REAL_OWNER
            )

            rtn = clientClass.upsert(clientData)
            self.assertEqual(rtn.status_code, 200)
            RT_JSON = rtn.json()
            self.assertIn('contactId', RT_JSON)
            self.assertIn('success', RT_JSON)
            self.assertTrue(RT_JSON['success'])
