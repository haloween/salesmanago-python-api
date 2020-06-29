from unittest import TestCase
from salesmanago_python_api.data.auth import SalesManagoAuthData


class SalesManagoAuthDataTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:

        self.auth = SalesManagoAuthData(
            apiKey="apiKey", 
            clientId="clientId",
            apiSecret="SEC"
        )

    def tearDown(self) -> None:
        pass

    def test_create_auth(self):
        auth = SalesManagoAuthData(apiKey="apiKey", clientId="clientId", apiSecret="SEC")
        self.assertEqual(auth.apiKey, "apiKey")
        self.assertEqual(auth.clientId, "clientId")
        self.assertEqual(auth.apiSecret, "SEC")

    def test_required_args(self):
        with self.assertRaises(TypeError):
            SalesManagoAuthData(
                clientId="clientId",
                apiSecret="SEC"
            )
        
        with self.assertRaises(TypeError):
            SalesManagoAuthData(
                apiKey="apiKey",
                apiSecret="SEC"
            )
        
        with self.assertRaises(TypeError):
            SalesManagoAuthData(
                apiKey="apiKey",
                clientId="SEC",
            )

    def test_get_requestTime(self):
        self.assertEqual(type(self.auth.requestTime), int)
        self.assertGreater(self.auth.requestTime, 0)

    def test_request_signature(self):
        self.assertEqual(type(self.auth.requestSignature), str)
        self.assertEqual(self.auth.requestSignature, '0336d993a5286afc0f00bf5228fa4f72be68c04b')

    def test_request_auth_data_dict(self):
        self.assertEqual(type(self.auth.requestAuthDict), dict)
        self.assertIn('apiKey', self.auth.requestAuthDict)
        self.assertIn('clientId', self.auth.requestAuthDict)
        self.assertIn('sha', self.auth.requestAuthDict)
        self.assertIn('requestTime', self.auth.requestAuthDict)

    def test_request_auth_data_dict_leaking(self):
        self.assertNotIn('apiSecret', self.auth.requestAuthDict)

    def test_str(self):
        self.assertEqual(str(self.auth), 'SalesManagoAuthData: apiKey')
