from unittest import TestCase
from tests import utils as tests_utils
from salesmanago_python_api.services.client import SalesManagoClientService
from salesmanago_python_api.data.client import SalesManagoClientData
from salesmanago_python_api.data.auth import SalesManagoAuthData


class SalesManagoClientTestBase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        apiKey = tests_utils.gen_string(12)
        clientId = tests_utils.gen_string(12)
        apiSecret = tests_utils.gen_string(12)
        serverDomain = 'app1.salesmanago.com'

        self.clientClass = SalesManagoClientService(
            apiKey=apiKey, clientId=clientId, 
            apiSecret=apiSecret, serverDomain=serverDomain
        )

        self.clientDataMock = self.clientClass.createClientData({
            'email': 'email@mail.pl',
            'owner': 'owner@mail.pl'
        })

    def tearDown(self) -> None:
        pass