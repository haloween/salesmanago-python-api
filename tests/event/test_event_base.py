from unittest import TestCase
from .text_data_mixin import EventTestDataMixin
from salesmanago_python_api.data.event import SalesManagoEventData
from salesmanago_python_api.data.client import SalesManagoClientData


class SalesManagoEventsTestsBase(TestCase, EventTestDataMixin):

    def setUp(self) -> None:
        self.mcd = self._min_event_data()
        self.fcd = self._full_event_data()

        self.eventClass = SalesManagoEventData(**self.mcd)
        self.eventClassFull = SalesManagoEventData(**self.fcd)

    def tearDown(self) -> None:
        pass