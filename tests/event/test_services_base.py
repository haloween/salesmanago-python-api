from unittest import TestCase
from tests import utils as tests_utils
from .text_data_mixin import EventTestDataMixin
from salesmanago_python_api.services.event import SalesManagoEventService
from salesmanago_python_api.data.event import SalesManagoEventData
from salesmanago_python_api.data.auth import SalesManagoAuthData


class SalesManagoEventsServiceTestBase(TestCase, EventTestDataMixin):

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

        self.clientClass = SalesManagoEventService(
            apiKey=apiKey, clientId=clientId, 
            apiSecret=apiSecret, serverDomain=serverDomain
        )

        self.clientDataMock = self.clientClass.createEventData(self._min_event_data())

    def tearDown(self) -> None:
        pass