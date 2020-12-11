# salesmanago-python-api

Python API for SalesManago integration.

## Installation

Install this library in a virtualenv using pip. virtualenv is a tool to create isolated Python environments. The basic problem it addresses is one of dependencies and versions, and indirectly permissions. With virtualenv, it's possible to install this library without needing system install permissions, and without clashing with the installed system dependencies.

### Mac/Linux

pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install salesmanago_python_api

### Windows

pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install salesmanago_python_api

### Supported Python Versions

Python 3.7, and 3.8 are fully supported and tested. This library may work on later versions of 3, but we do not currently run tests against those versions

Deprecated Python Versions
Python <= 3.7

## Third Party Libraries and Dependencies

The following libraries will be installed when you install the client library:

requests

## Services

Currently client service is supported PARTIALLY, event service is supported only for inserts.
I've needed only a few methods and those were implemented.

`SalesManagoClientService` handles:

* insert
* upsert
* update
* delete

`SalesManagoClientService` handles:

* addContactExtEvent
* batchAddContactExtEvent


## Usage of Client Service

Start with import ;)
`from salesmanago_python_api.services import SalesManagoClientService`

Since SalesManago has different data requirements for all supported methods, it's required to interface with the client service using `SalesManagoClientData` class. 
It will handle all the required formatting for you.

```python

clientServiceClass = SalesManagoClientService(
    apiKey=API_KEY,
    clientId=CLIENT_ID,
    apiSecret=API_SECRET,
    serverDomain=SERVER_DOMAIN
)

clientDataClass = clientServiceClass.ClientData
clientData = clientDataClass(
    email='unittest@salesmanagopythonapi.pl',
    owner=REAL_OWNER
)

response = clientServiceClass.insert(clientData)
response.raise_for_status()
response_json = response.json()

```

`SalesManagoClientService` needs to be initialized only once, it setups requests Session and handles the request build process.

```python

clientServiceClass = SalesManagoClientService(
    apiKey=API_KEY,
    clientId=CLIENT_ID,
    apiSecret=API_SECRET,
    serverDomain=SERVER_DOMAIN
)

#insert new client into SM database.
clientDataClass = clientServiceClass.ClientData
clientData = clientDataClass(
    email='client@salesmanagopythonapi.pl',
    owner='owner@company.com'
)
clientServiceClass.insert(clientData)


#update SM client with newMail and state
clientUpdateData = clientDataClass(
    email='client@salesmanagopythonapi.pl',
    owner='owner@company.com',
    state='CUSTOMER',
    newMail='newmail@salesmanagopythonapi.pl'
)
clientServiceClass.update(clientUpdateData)

#delete him
clientDeleteData = clientDataClass(
    email='newmail@salesmanagopythonapi.pl',
    owner='owner@company.com'
)
clientServiceClass.delete(clientData)

```

## Properties on SalesManagoClientData

* email: str - Required Contact E-mail
* owner: str - Required Owner E-mail
* state: str - one of ['CUSTOMER', 'PROSPECT', 'PARTNER', 'OTHER', 'UNKNOWN]
* name: Optional[str]
* phone: Optional[str]
* fax: Optional[str]
* company: Optional[str]
* externalId: Optional[str]
* newEmail: Optional[str]
* birthday: Optional[datetime.date]
* address_streetAddress: Optional[str]
* address_zipCode: Optional[str]
* address_city: Optional[str]
* address_country: Optional[str]
* lang: Optional[str]
* tags: list = field(default_factory=list)
* removeTags: list = field(default_factory=list)
* forceOptOut: bool
* forceOptIn: bool
* forcePhoneOptOut: bool
* forcePhoneOptIn: bool
* useApiDoubleOptIn: bool
* properties: dict = field(default_factory=dict)
* province: str

### Tags / removeTags and properties

Tags and removeTags have nice methods:

```python
clientData.add_tag('XXX')
clientData.remove_tag('XXX')

clientData.add_removeTags('XXX')
clientData.remove_removeTags('XXX')
```

Properties have those too :)

```python
clientData.add_property('key', 'value')
clientData.remove_property('key')
```

## Running tests VS real API

To run real tests vs REAL API some enviroment variables need to be set:

* TEST_REAL_API -> True
* REAL_API_KEY
* REAL_API_SECRET
* REAL_CLIENT_ID
* REAL_OWNER
* REAL_SERVER_DOMAIN

To set enviroment variables use `set` in Linux or `export` in Windows.
