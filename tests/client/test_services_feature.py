import random
import string
import requests
from unittest.mock import patch
from tests import utils as tests_utils
from .test_services_base import SalesManagoClientTestBase
from salesmanago_python_api.services.client import SalesManagoClientService
from salesmanago_python_api.data.client import SalesManagoClientData
from salesmanago_python_api.data.auth import SalesManagoAuthData


class SalesManagoClientFeatureTest(SalesManagoClientTestBase):
    pass

    @patch.object(SalesManagoClientService, 'insert')
    def test_insert_action(self, mock_get) -> None:
        mock_get.return_value.status_code = 200
        self.clientClass.insert(self.clientDataMock)
