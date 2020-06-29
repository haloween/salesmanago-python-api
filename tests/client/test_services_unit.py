import requests
from tests import utils as tests_utils
from .test_services_base import SalesManagoClientTestBase
from salesmanago_python_api.data.auth import SalesManagoAuthData
from salesmanago_python_api.data.client import SalesManagoClientData
from salesmanago_python_api.services.client import SalesManagoClientService


class SalesManagoClientTest(SalesManagoClientTestBase):

    def test_client_class_basic_init(self) -> None:
        apiKey = tests_utils.gen_string(12)
        clientId = tests_utils.gen_string(12)
        apiSecret = tests_utils.gen_string(12)
        serverDomain = 'app1.salesmanago.com'

        clientClass = SalesManagoClientService(
            apiKey=apiKey, clientId=clientId, 
            apiSecret=apiSecret, serverDomain=serverDomain
        )

        self.assertEqual(clientClass.apiKey, apiKey)
        self.assertEqual(clientClass.clientId, clientId)
        self.assertEqual(clientClass.apiSecret, apiSecret)
        self.assertEqual(clientClass.serverDomain, serverDomain)

    def test_client_class_validate_server_url(self) -> None:
        apiKey = tests_utils.gen_string(12)
        clientId = tests_utils.gen_string(12)
        apiSecret = tests_utils.gen_string(12)

        with self.assertRaises(ValueError):
            serverDomain = tests_utils.gen_string(12)
            clientClass = SalesManagoClientService(
                apiKey=apiKey, clientId=clientId, 
                apiSecret=apiSecret, serverDomain=serverDomain
            )

    def test_client_class_authdata_init(self) -> None:
        self.assertIsInstance(self.clientClass._authData, SalesManagoAuthData)

    def test_client_class_get_client_data_class(self) -> None:
        self.assertIs(self.clientClass.ClientData, SalesManagoClientData)

    def test_client_class_create_client_data_instance(self) -> None:
        self.assertIsInstance(self.clientClass.createClientData({
            'email': 'email@mail.pl',
            'owner': 'owner@mail.pl'
        }), SalesManagoClientData)

    def test_generate_request_payload_insert_accepts_only_clientdata(self) -> None:
        with self.assertRaises(TypeError):
            self.clientClass._generate_payload({}, 'insert')

    def test_generate_request_payload_insert_returns_dict(self) -> None:
        self.assertIsInstance(self.clientClass._generate_payload(self.clientDataMock, 'insert'), dict)

    def test_generate_request_payload_update_accepts_only_clientdata(self) -> None:
        with self.assertRaises(TypeError):
            self.clientClass._generate_payload({}, 'update')

    def test_generate_request_payload_update_dict(self) -> None:
        self.assertIsInstance(self.clientClass._generate_payload(self.clientDataMock, 'update'), dict)

    def test_generate_request_payload_insert_has_required_properties(self) -> None:
        payload = self.clientClass._generate_payload(self.clientDataMock, 'insert')
        self.assertIn('contact', payload)
        self.assertIn('email', payload['contact'])
        self.assertIn('owner', payload)
        self.assertIn('apiKey', payload)
        self.assertIn('clientId', payload)
        self.assertIn('sha', payload)
        self.assertIn('requestTime', payload)
        self.assertNotIn('apiSecret', payload)
    
    def test_generate_request_payload_update_has_required_properties(self) -> None:
        payload = self.clientClass._generate_payload(self.clientDataMock, 'update')
        self.assertIn('email', payload)
        self.assertIn('owner', payload)
        self.assertIn('apiKey', payload)
        self.assertIn('clientId', payload)
        self.assertIn('sha', payload)
        self.assertIn('requestTime', payload)
        self.assertNotIn('apiSecret', payload)

    def test_request_session_setup(self):
        self.assertIsInstance(self.clientClass.session_setup(), requests.Session)
        self.assertIsInstance(self.clientClass._requestsSession, requests.Session)

    def test_request_session_present_after_init(self):
        self.assertIsInstance(self.clientClass._requestsSession, requests.Session)

    def test_request_session_proper_headers(self):
        rsession_headers = self.clientClass._requestsSession.headers
        self.assertIn('Accept', rsession_headers)
        self.assertIn('Content-Type', rsession_headers)
        self.assertEqual(rsession_headers['Accept'], 'application/json, application/json')
        self.assertEqual(rsession_headers['Content-Type'], 'application/json;charset=UTF-8')

    def test_insert_takes_only_clientData(self):
        with self.assertRaises(TypeError):
            self.clientClass.insert({})

    def test_generate_request_requires_action(self):
        with self.assertRaises(TypeError):
            self.clientClass._generate_request(self.clientDataMock)
    
    def test_generate_request_action_is_validated(self):
        with self.assertRaises(ValueError):
            self.clientClass._generate_request(self.clientDataMock, action='fail')

    def test_generate_request_takes_only_clientData(self):
        with self.assertRaises(TypeError):
            self.clientClass._generate_request({}, action='insert')

    def test_generate_request_return(self) -> None:
        self.assertIsInstance(
            self.clientClass._generate_request(self.clientDataMock, action='insert'), 
            requests.PreparedRequest
        )

    def test_generate_request_handle_invalid_method_arg(self) -> None:
        with self.assertRaises(ValueError):
            self.clientClass._generate_request(
                self.clientDataMock, action='insert', method='FAIL'
            )

    def test_generate_request_handle_valid_method_arg(self) -> None:
        self.assertIsInstance(
            self.clientClass._generate_request(
                self.clientDataMock, action='insert', method='GET'
            ), 
            requests.PreparedRequest
        )
