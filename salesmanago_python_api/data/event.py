import re
import datetime
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class SalesManagoEventData:
    '''
        Class for interfacing with event instances of SalesManago platform.
        Structure is valid for following API actions: /api/v2/contact/addContactExtEvent
    '''

    contactExtEventType: str
    _contactExtEventType: str = field(init=False, repr=False, default=None)

    eventDate: int
    _eventDate: int = field(init=False, repr=False, default=None)

    owner: str
    _owner: str = field(init=False, repr=False, default=None)

    contactId: Optional[str] = None

    email: Optional[str] = None
    _email: str = field(init=False, repr=False, default=None)

    #extra stuff
    forceOptIn: Optional[bool] = None
    description: Optional[str] = None
    products: Optional[str] = None
    location: Optional[str] = None
    value: Optional[str] = None
    detail1: Optional[str] = None
    detail2: Optional[str] = None
    detail3: Optional[str] = None
    detail4: Optional[str] = None
    detail5: Optional[str] = None
    detail6: Optional[str] = None
    detail7: Optional[str] = None
    detail8: Optional[str] = None
    detail9: Optional[str] = None
    detail10: Optional[str] = None
    detail11: Optional[str] = None
    detail12: Optional[str] = None
    detail13: Optional[str] = None
    detail14: Optional[str] = None
    detail15: Optional[str] = None
    detail16: Optional[str] = None
    detail17: Optional[str] = None
    detail18: Optional[str] = None
    detail19: Optional[str] = None
    detail20: Optional[str] = None
    externalId: Optional[str] = None
    shopDomain: Optional[str] = None

    VALID_EVENTS = [
        'PURCHASE', 'CART', 'VISIT', 'PHONE_CALL', 'OTHER', 'RESERVATION', 'CANCELLED', 
        'ACTIVATION', 'MEETING', 'OFFER', 'DOWNLOAD', 'LOGIN', 'TRANSACTION', 'CANCELLATION', 
        'RETURN', 'SURVEY', 'APP_STATUS', 'APP_TYPE_WEB', 'APP_TYPE_MANUAL', 'APP_TYPE_RETENTION', 
        'APP_TYPE_UPSALE', 'LOAN_STATUS', 'LOAN_ORDER', 'FIRST_LOAN', 'REPEATED_LOAN'
    ]

    def __post_init__(self):
        if not self.owner:
            raise ValueError('owner[str] is required')

        if not self.email and not self.contactId:
            raise ValueError('email[str] or contactId[str] is required')
        
        if not self.eventDate:
            raise ValueError('eventDate[int] timestamp is required')
            
        if not self.contactExtEventType:
            raise ValueError('contactExtEventType[str] is required')

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        if type(email) is property:
            email = self._email

        if email and not self._validate_email(email):
            raise ValueError(' %s is not valid CLIENT e-mail' % email)

        self._email = email

    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, owner: str) -> None:
        if type(owner) is property:
            owner = self._owner

        if owner and not self._validate_email(owner):
            raise ValueError('%s is not valid OWNER e-mail' % owner)

        self._owner = owner
    
    def _validate_email(self, email):
        mailre = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return mailre.match(email)

    @property
    def eventDate(self) -> str:
        return self._eventDate

    @eventDate.setter
    def eventDate(self, eventDate: int) -> None:
        if type(eventDate) is property:
            eventDate = self._eventDate

        if eventDate and not isinstance(eventDate, int):
            raise TypeError('eventDate should be int, not %s' % type(eventDate))

        self._eventDate = eventDate

    @property
    def contactExtEventType(self) -> str:
        return self._contactExtEventType

    @contactExtEventType.setter
    def contactExtEventType(self, contactExtEventType: str) -> None:
        if type(contactExtEventType) is property:
            contactExtEventType = self._contactExtEventType

        if contactExtEventType and contactExtEventType not in self.VALID_EVENTS:
            raise ValueError('contactExtEventType should be on of %s' % self.VALID_EVENTS)

        self._contactExtEventType = contactExtEventType
    
    def requestDict(self) -> dict:

        ALL_ATTRS = [
            'owner', 'email', 'contactId', 'forceOptIn'
        ]

        CONTACT_EVENT_ATTRS = [
            'description', 'products', 'location', 'value', 'externalId', 'shopDomain'
        ]

        CONTACT_EVENT_ATTRS.extend(['detail%s' % did for did in range(1,21)])

        rdata = {
            k: getattr(self, k) for k in ALL_ATTRS if hasattr(self, k) and getattr(self, k) is not None
        }

        rdata['contactEvent'] = {
            k: getattr(self, k) for k in CONTACT_EVENT_ATTRS if hasattr(self, k) and getattr(self, k) is not None
        }

        rdata['contactEvent']["contactExtEventType"] = self.contactExtEventType
        rdata['contactEvent']["date"] = self.eventDate

        return rdata
