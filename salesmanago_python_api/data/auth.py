import hashlib
from datetime import datetime
from dataclasses import dataclass


@dataclass
class SalesManagoAuthData:
    apiKey: str
    clientId: str
    apiSecret: str

    def __str__(self) -> str:
        return 'SalesManagoAuthData: %s' % self.apiKey

    @property
    def requestTime(self) -> int:
        '''
            Request time for sending stuff.
        '''
        return int(datetime.now().timestamp())

    @property
    def requestSignature(self) -> str:
        '''
            The sha value is generated using the SHA-1 algorithm from a string 
            created from the combination: apiKey + clientId + apiSecret.
        '''
        hl = hashlib.sha1()
        hl.update(self.apiKey.encode('utf-8'))
        hl.update(self.clientId.encode('utf-8'))
        hl.update(self.apiSecret.encode('utf-8'))
        return hl.hexdigest()

    @property
    def requestAuthDict(self) -> dict:
        '''
            Returns dict to auth feed all of requests.
        '''
        return {
            'apiKey': self.apiKey,
            'clientId': self.clientId,
            'sha': self.requestSignature,
            'requestTime': self.requestTime
        }