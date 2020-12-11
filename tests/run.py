import sys, os
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
TOP_DIR = os.path.dirname(FILE_PATH)
sys.path.insert(0, TOP_DIR)


from auth.test_unit import SalesManagoAuthDataTest

from client.test_data_unit import SalesManagoClientDataUnitTest
from client.test_data_feature import SalesManagoClientDataFeatureTest

from client.test_services_unit import SalesManagoClientTest
from client.test_services_integration import SalesManagoClientIntegrationTest

from event.test_data_unit import SalesManagoEventDataUnitTest
from event.test_data_feature import SalesManagoEventDataFeatureTest

from event.test_services_unit import SalesManagoEventServiceUnitTest

#from event.test_event_services_integration import SalesManagoEventIntegrationTest

if __name__ == "__main__":
    import unittest
    unittest.main()