import re
import json
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from salesmanago_python_api.data.auth import SalesManagoAuthData
from salesmanago_python_api.data.event import SalesManagoEventData


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class SalesManagoEventService:

    API_RETRY_COUNT = 1
    API_BACKOFF_FACTOR = 1
    API_REQUEST_DEFAULT_TIMEOUT = 2

    ACTION_URLS = {
        'addContactExtEvent': '/api/v2/contact/addContactExtEvent',
        'batchAddContactExtEvent': '/api/contact/batchAddContactExtEvent'
    }

    def __init__(self, apiKey, clientId, apiSecret, serverDomain):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.clientId = clientId

        url_regex = re.compile('^([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}$', re.IGNORECASE)
        if not url_regex.match(serverDomain):
            raise ValueError('serverDomain is invalid, provide like appx.salesmanago.xxx')

        self.serverDomain = serverDomain

        logger.debug(json.dumps({
            'action': '__init__',
            'apiKey': apiKey,
            'clientId': clientId,
            'apiSecret': apiSecret,
            'serverDomain': serverDomain
        }))

        self._authData = SalesManagoAuthData(
            apiKey = apiKey,
            apiSecret = apiSecret,
            clientId = clientId
        )

        self.session_setup(
            retries=self.API_RETRY_COUNT, 
            backoff_factor=self.API_BACKOFF_FACTOR
        )
    
    _requestsSession = None
    def session_setup(self, retries=1, backoff_factor=1, status_forcelist=(500, 502, 504),):
        session = requests.Session()

        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )

        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        session.headers.update({
            'Accept': 'application/json, application/json',
            'Content-Type': 'application/json;charset=UTF-8'
        })

        self._requestsSession = session
        return session
    
    @property
    def EventData(self):
        return SalesManagoEventData
    
    def createEventData(self, event_data):
        logger.debug(json.dumps({
            'action': 'createClientData',
            'client_data': event_data
        }))

        return self.EventData(**event_data)
    
    def _generate_payload(self, eventData, request_type):
        payload = self._authData.requestAuthDict
        processed = False

        if request_type not in self.ACTION_URLS.keys():
            raise ValueError('request_type should be one of %s' % self.ACTION_URLS.keys())
        
        if request_type == 'addContactExtEvent':
            if not isinstance(eventData, self.EventData):
                raise TypeError('addContactExtEvent payload accepts only SalesManagoEventData instance, call .EventData or .createEventData')
                
            payload.update(eventData.requestDict())
            processed = True
        
        if request_type == 'batchAddContactExtEvent':
            if type(eventData) != type([]) :
                raise TypeError('batchAddContactExtEvent payload accepts only array of SalesManagoEventData instances, call .EventData or .createEventData')
            
            for event in eventData:
                if not isinstance(event, self.EventData):
                    raise TypeError('batchAddContactExtEvent payload accepts only array of SalesManagoEventData instances, call .EventData or .createEventData')
            
            if len(set([ed.owner for ed in eventData])) > 1:
                raise ValueError('batchAddContactExtEvent payload should all have the same owner !')
            
            payload['events'] = []
            
            for ed in eventData:
                rd = ed.requestDict()
                payload['owner'] = rd['owner']
                del rd['owner']
                payload['events'].append(rd)

            processed = True

        logger.debug(json.dumps({
            'action': '_generate_payload',
            'payload': payload
        }))

        if processed:
            return payload

    def addContactExtEvent(self, eventData):
        
        if not isinstance(eventData, self.EventData):
            raise TypeError('addContactExtEvent accepts only SalesManagoEventData instances')
        
        request = self._generate_request(eventData, 'addContactExtEvent')
        response = self._requestsSession.send(
            request,
            timeout=self.API_REQUEST_DEFAULT_TIMEOUT
        )

        logger.debug(json.dumps({
            'action': 'addContactExtEvent',
            'request_body': request.body,
            'response_status': response.status_code,
            'response_json': response.json(),
            'eventData': eventData.requestDict('addContactExtEvent')
        }))

        return response

    def _generate_request(self, eventData, action, method='POST'):

        logger.debug(json.dumps({
            'action': '_generate_request',
            'action': action,
            'method': method
        }))

        ALLOWED_ACTIONS = [k for k,v in self.ACTION_URLS.items()]
        if action not in ALLOWED_ACTIONS:
            raise ValueError('action must be on of %s' % ALLOWED_ACTIONS)
        
        ALLOWED_METHODS = ['GET', 'POST']
        if method not in ALLOWED_METHODS:
            raise ValueError('method must be on of %s' % ALLOWED_METHODS)

        url = 'https://{server}{action}'.format(
            server=self.serverDomain,
            action=self.ACTION_URLS[action]
        )

        payload = self._generate_payload(eventData, action)

        rq = requests.Request(
            method=method, 
            url=url,
            data=json.dumps(payload)
        )

        return self._requestsSession.prepare_request(rq)
    
    def batchAddContactExtEvent(self, eventData):

        if type(eventData) is not type([]):
            raise TypeError('batchAddContactExtEvent accepts only array of SalesManagoEventData instances')
        
        request = self._generate_request(eventData, 'batchAddContactExtEvent')
        response = self._requestsSession.send(
            request,
            timeout=self.API_REQUEST_DEFAULT_TIMEOUT
        )

        logger.debug(json.dumps({
            'action': 'batchAddContactExtEvent',
            'request_body': request.body,
            'response_status': response.status_code,
            'response_json': response.json(),
            'eventData': [ed.requestDict() for ed in eventData]
        }))

        return response
