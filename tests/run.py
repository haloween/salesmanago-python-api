import sys, os
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TOP_DIR = os.path.dirname(FILE_PATH)
sys.path.insert(0, TOP_DIR)


from auth.test_unit import SalesManagoAuthDataTest

from client.test_data_unit import SalesManagoClientDataUnitTest
from client.test_data_feature import SalesManagoClientDataFeatureTest

from client.test_services_unit import SalesManagoClientTest
from client.test_services_integration import SalesManagoClientIntegrationTest

from client.test_data_event_unit import SalesManagoEventDataUnitTest
from client.test_data_event_feature import SalesManagoClientDataFeatureTest


if __name__ == "__main__":
    import unittest
    unittest.main()