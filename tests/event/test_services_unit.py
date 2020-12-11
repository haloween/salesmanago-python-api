import requests
from tests import utils as tests_utils
from .test_services_base import SalesManagoEventsServiceTestBase
from salesmanago_python_api.data.auth import SalesManagoAuthData
from salesmanago_python_api.data.event import SalesManagoEventData
from salesmanago_python_api.services.event import SalesManagoEventService


class SalesManagoEventServiceUnitTest(SalesManagoEventsServiceTestBase):

    def test_client_class_basic_init(self) -> None:
        apiKey = tests_utils.gen_string(12)
        clientId = tests_utils.gen_string(12)
        apiSecret = tests_utils.gen_string(12)
        serverDomain = 'app1.salesmanago.com'

        clientClass = SalesManagoEventService(
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
            clientClass = SalesManagoEventService(
                apiKey=apiKey, clientId=clientId, 
                apiSecret=apiSecret, serverDomain=serverDomain
            )

    #BASIC AUTH
    def test_client_class_authdata_init(self) -> None:
        self.assertIsInstance(self.clientClass._authData, SalesManagoAuthData)

    #CLIENT DATA HELPERS
    def test_client_class_get_client_data_class(self) -> None:
        self.assertIs(self.clientClass.EventData, SalesManagoEventData)

    def test_client_class_create_client_data_instance(self) -> None:
        self.assertIsInstance(self.clientClass.createEventData(self._min_event_data()), SalesManagoEventData)

    #CLIENT - SESSION
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

    #CLIENT STUFF - PAYLOAD TYPECHECKS
    def test_generate_request_payload_addContactExtEvent_accepts_valid_request_type(self) -> None:
        with self.assertRaises(ValueError):
            for x in range(0,10):
                self.clientClass._generate_payload({}, tests_utils.gen_string(12))

    #addContactExtEvent
    def test_generate_request_payload_addContactExtEvent_accepts_only_eventdata(self) -> None:
        with self.assertRaises(TypeError):
            self.clientClass._generate_payload({}, 'addContactExtEvent')
    
    #batchAddContactExtEvent
    def test_generate_request_payload_batchAddContactExtEvent_accepts_only_eventdata_array(self) -> None:
        with self.assertRaises(TypeError):
            self.clientClass._generate_payload({}, 'batchAddContactExtEvent')

    #quirk    
    def test_generate_request_payload_batchAddContactExtEvent_checks_same_owner(self) -> None:
        events = []

        for x in range(0,10):
            dt = self._min_event_data(fields=['contactId', 'eventDate', 'contactExtEventType'])
            dt['owner'] = '%s@%s.com' % (tests_utils.gen_string(16), tests_utils.gen_string(4))

            events.append(
                self.clientClass.createEventData(dt)
            )

        with self.assertRaises(ValueError):
            self.clientClass._generate_payload(events, 'batchAddContactExtEvent')

    #CLIENT STUFF - PROPS CHECKS
    def test_generate_request_payload_addContactExtEvent_has_required_properties(self) -> None:
        '''
        REFERENCE
        {
            "clientId":"your-client-id-123",
            "apiKey":"your-api-key-123",
            "requestTime":1356180568127,
            "sha":"3e4ec39722326150aae60f41e038d1def4450f46",
            "owner":"admin@vendor.pl",
            "email":"test@benhauer.com",
            "forceOptIn": true,
            "contactEvent":{
                "date":1356180568153,
                "description":"Purchase card \"Super Bonus\"",
                "products":"p01, p02",
                "location":"Shop_ID",
                "value":1234.43,
                "contactExtEventType":"PURCHASE",
                "detail1":"C.ID: *** *** 234",
                "detail2":"Payment by credit card",
                "detail3":null,
                "externalId":"A-123123123",
                "shopDomain":"shop.salesmanago.pl"
            }
        }
        '''

        payload = self.clientClass._generate_payload(self.clientDataMock, 'addContactExtEvent')
        self.assertIsInstance(payload, dict)
        self.assertIn('clientId', payload)
        self.assertIn('apiKey', payload)
        self.assertIn('requestTime', payload)
        self.assertIn('sha', payload)
        self.assertIn('owner', payload)
        self.assertIn('email', payload)
        self.assertIn('contactEvent', payload)
        self.assertIn('date', payload['contactEvent'])
        self.assertIn('contactExtEventType', payload['contactEvent'])
        
    
    #CLIENT STUFF - PROPS CHECKS
    def test_generate_request_payload_batchAddContactExtEvent_has_proper_return(self) -> None:
        '''
        REFERENCE
        {
            "clientId": "your-client-id-123",
            "apiKey": "your-api-key-123",
            "sha": "09b42a100849de3e4f7fad4f445eb47e833dba87",
            "requestTime":1327056031488,
            "owner":"user@vendor.pl",
            "events": [
                    {
                        "contactId":"001e720f-b2ab-4203-a25f-b089557cf0da",
                        "contactEvent":{
                            "date":356180568153,
                            "description":"Bought with \"Super Bonus\"",
                            "products":"p01, p02",
                            "location":"Shop_ID",
                            "value":1234.43,
                            "contactExtEventType":"PURCHASE",
                            "detail1":"C.ID: *** *** 234",
                            "detail2":"Paid with card",
                            "detail3":null,
                            "externalId":"B-99999999",
                            "shopDomain":"shop.salesmanago.pl"
                        }   
                    }
                ]
            }
        '''

        payload = self.clientClass._generate_payload([self.clientDataMock], 'batchAddContactExtEvent')
        
        self.assertIsInstance(payload, dict)
        self.assertIn('clientId', payload)
        self.assertIn('apiKey', payload)
        self.assertIn('requestTime', payload)
        self.assertIn('sha', payload)
        self.assertIn('events', payload)
        self.assertIn('owner', payload)
        self.assertNotIn('email', payload)
        self.assertNotIn('contactEvent', payload)
        self.assertNotIn('contactExtEventType', payload)
        self.assertIs(type(payload['events']), type([]))
        #contact check
        for eData in payload['events']:
            self.assertNotIn('owner', eData)

    #CLIENT - REQUEST PAYLOADS
    def test_addContactExtEvent_takes_only_eventData(self):
        with self.assertRaises(TypeError):
            self.clientClass.addContactExtEvent({})
    
    def test_batchAddContactExtEvent_takes_only_eventData_array(self):
        '''
            More checks are performed in generate payload etc..
        '''
        with self.assertRaises(TypeError):
            self.clientClass.batchAddContactExtEvent({})

    def test_generate_request_requires_action(self):
        with self.assertRaises(TypeError):
            self.clientClass._generate_request(self.clientDataMock)
    
    def test_generate_request_requires_valid_action(self):
        with self.assertRaises(ValueError):
            self.clientClass._generate_request(self.clientDataMock, action='fail')

    def test_generate_request_returns_prepared_request(self) -> None:
        self.assertIsInstance(
            self.clientClass._generate_request(self.clientDataMock, action='addContactExtEvent'), 
            requests.PreparedRequest
        )

    def test_generate_request_handle_invalid_method_arg(self) -> None:
        with self.assertRaises(ValueError):
            self.clientClass._generate_request(
                self.clientDataMock, action='addContactExtEvent', method='FAIL'
            )

    def test_generate_request_handle_valid_method_arg(self) -> None:
        self.assertIsInstance(
            self.clientClass._generate_request(
                self.clientDataMock, action='addContactExtEvent', method='GET'
            ), 
            requests.PreparedRequest
        )