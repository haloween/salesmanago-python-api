import re
import datetime
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class SalesManagoClientData:
    '''
        Class for interfacing with client instances of SalesManago platform.
        Structure was valid for following API actions: insert / upsert / update / batchupsert
    '''

    email: str
    _email: str = field(init=False, repr=False, default=None)

    owner: str
    _owner: str = field(init=False, repr=False, default=None)

    state: Optional[str] = None
    _state: str = field(init=False, repr=False, default=None)

    name: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    company: Optional[str] = None
    externalId: Optional[str] = None
    newEmail: Optional[str] = None
    _newEmail: str = field(init=False, repr=False, default=None)
    birthday: Optional[datetime.date]
    _birthday: datetime.date = field(init=False, repr=False, default=None)
    address_streetAddress: Optional[str] = None
    address_zipCode: Optional[str] = None
    address_city: Optional[str] = None
    address_country: Optional[str] = None
    lang: Optional[str] = None
    tags: list = field(default_factory=list)
    removeTags: list = field(default_factory=list)
    forceOptOut: bool = None
    forceOptIn: bool = None
    forcePhoneOptOut: bool = None
    forcePhoneOptIn: bool = None
    useApiDoubleOptIn: bool = None
    properties: dict = field(default_factory=dict)
    province: str = None

    VALID_STATES = ['CUSTOMER', 'PROSPECT', 'PARTNER', 'OTHER', 'UNKNOWN']

    def __post_init__(self):
        if not self.owner:
            raise ValueError('owner is required')

        if self.tags and not isinstance(self.tags, list):
            raise TypeError('tags should be a list')
        
        if self.removeTags and not isinstance(self.removeTags, list):
            raise TypeError('removeTags should be a list')

        if self.properties and not isinstance(self.properties, dict):
            raise TypeError('properties should be a list')

    def _validate_email(self, email):
        mailre = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return mailre.match(email)
    
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

    @property
    def newEmail(self) -> str:
        return self._newEmail

    @newEmail.setter
    def newEmail(self, newEmail: str) -> None:
        if type(newEmail) is property:
            newEmail = self._newEmail

        if newEmail and not self._validate_email(newEmail):
            raise ValueError(' %s is not valid NEW e-mail' % self.newEmail)

        self._newEmail = newEmail

    @property
    def birthday(self) -> str:
        return self._birthday

    @birthday.setter
    def birthday(self, birthday: datetime.date) -> None:
        if type(birthday) is property:
            birthday = self._birthday

        if birthday and not isinstance(birthday, datetime.date):
            raise TypeError('birthday should be datetime.date, not %s' % type(birthday))

        self._birthday = birthday

    @property
    def birthDateConverted(self):
        if not self._birthday:
            return None

        return self._birthday.strftime('%Y%m%d')

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, state: str) -> None:
        if type(state) is property:
            state = self._state

        if state and state not in self.VALID_STATES:
            raise ValueError('state should be on of %s' % self.VALID_STATES)

        self._state = state

    def add_tag(self, tag:str) -> None:
        self.tags.append(tag)

    def remove_tag(self, tag:str) -> None:
        self.tags.remove(tag)

    def add_removeTags(self, tag:str) -> None:
        self.removeTags.append(tag)

    def remove_removeTags(self, tag:str) -> None:
        self.removeTags.remove(tag)

    def add_property(self, key: str, value: str) -> None:
        self.properties[key] = value

    def remove_property(self, key: str) -> None:
        del self.properties[key]

    @property
    def address(self) -> dict:
        ADDRESS_ATTRS = [
            'address_streetAddress',
            'address_zipCode',
            'address_city',
            'address_country',
        ]

        if not any([getattr(self, key) for key in ADDRESS_ATTRS]):
            return None

        return {
            k.replace('address_', ''): getattr(self, k) for k in ADDRESS_ATTRS if getattr(self, k)
        }

    def contact(self, request_format) -> dict:
        CONTACT_ATTRS = [
            'email',
            'fax',
            'name',
            'phone',
            'company',
            'state',
            'address'
        ]

        if request_format == 'update':
            CONTACT_ATTRS.remove('email')

        return {
            k: getattr(self, k) for k in CONTACT_ATTRS if getattr(self, k) is not None
        }

    ALLOWED_FORMATS = ['insert', 'update', 'delete', 'upsert']

    def requestDict(self, request_format) -> dict:

        if request_format not in self.ALLOWED_FORMATS:
            raise ValueError('Allowed formats are %s' % self.ALLOWED_FORMATS)

        #delete is super short
        if request_format == 'delete':
            return {
                'email': self.email,
                'owner': self.owner
            }

        ALL_ATTRS = [
            'owner', 'externalId', 'newEmail',  'lang', 'forceOptOut', 'forceOptIn', 
            'forcePhoneOptOut', 'forcePhoneOptIn', 'useApiDoubleOptIn', 'province', 'birthday'
        ]

        ITERABLE_ATTRS = [
            'tags', 'removeTags', 'properties'
        ]

        rdata = {
            k: getattr(self, k) for k in ALL_ATTRS if hasattr(self, k) and getattr(self, k) is not None
        }

        rdata.update({
            k: getattr(self, k) for k in ITERABLE_ATTRS if any(getattr(self, k))
        })

        c_data = self.contact(request_format)
        if any(c_data):
            rdata['contact'] = c_data

        if self.birthday:
            rdata['birthday'] = self.birthDateConverted

        #those requests need to have email on them ...
        if request_format == 'update':
            rdata['email'] = self.email

        if request_format == 'upsert':
            rdata['email'] = self.email

        return rdata
