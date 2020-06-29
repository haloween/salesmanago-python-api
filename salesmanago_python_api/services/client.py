import re
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from salesmanago_python_api.data.auth import SalesManagoAuthData
from salesmanago_python_api.data.client import SalesManagoClientData


class SalesManagoClientService:

    API_RETRY_COUNT = 1
    API_BACKOFF_FACTOR = 1
    API_REQUEST_DEFAULT_TIMEOUT = 2

    ACTION_URLS = {
        'insert': '/api/contact/insert',
        'upsert': '/api/contact/upsert',
        'update': '/api/contact/update'
    }

    def __init__(self, apiKey, clientId, apiSecret, serverDomain):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.clientId = clientId

        url_regex = re.compile('^([A-Za-z0-9]\.|[A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9]\.){1,3}[A-Za-z]{2,6}$', re.IGNORECASE)
        if not url_regex.match(serverDomain):
            raise ValueError('serverDomain is invalid, provide like appx.salesmanago.xxx')

        self.serverDomain = serverDomain
        self._authData = SalesManagoAuthData(
            apiKey = apiKey,
            apiSecret = apiSecret,
            clientId = clientId
        )

        self.session_setup(
            retries=self.API_RETRY_COUNT, 
            backoff_factor=self.API_BACKOFF_FACTOR
        )

    @property
    def ClientData(self):
        return SalesManagoClientData

    def createClientData(self, client_data):
        return self.ClientData(**client_data)

    def _generate_payload(self, clientData):
        if not isinstance(clientData, self.ClientData):
            raise TypeError('payload accepts only SalesManagoClientData instances, call .ClientData or .createClientData')

        payload = self._authData.requestAuthDict
        payload.update(clientData.requestDict)
        return payload

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
    
    def _generate_request(self, clientData, action, method='GET'):

        if not isinstance(clientData, self.ClientData):
            raise TypeError('_generate_request accepts only SalesManagoClientData instances')
        
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

        rq = requests.Request(
            method=method, 
            url=url,
            data=self._generate_payload(clientData)
        )

        return rq

    def insert(self, clientData):
        if not isinstance(clientData, self.ClientData, 'insert'):
            raise TypeError('insert accepts only SalesManagoClientData instances')

        request = self._generate_request(clientData)
        response = self._requestsSession.send(
            request,
            timeout=self.API_REQUEST_DEFAULT_TIMEOUT
        )
        return response

