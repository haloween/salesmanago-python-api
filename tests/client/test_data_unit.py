from unittest import TestCase
from .test_data_base import SalesManagoTestsBase
from tests.utils import gen_list_of_strings, gen_dict
from salesmanago_python_api.data.client import SalesManagoClientData


class SalesManagoClientDataUnitTest(SalesManagoTestsBase):

    def test_create_minimal_client(self):
        clientClass = SalesManagoClientData(email=self.CLIENT_MAIL, owner=self.OWNER_MAIL)
        self.assertEqual(clientClass.email, self.CLIENT_MAIL)
        self.assertEqual(clientClass.owner, self.OWNER_MAIL)

    def test_email_validated_on_create(self):
        with self.assertRaises(ValueError):
            for invalid_email in self.INVALID_MAILS:
                SalesManagoClientData(email=invalid_email, owner=self.VALID_MAIL)

    def test_email_validated_on_change(self):
        with self.assertRaises(ValueError):
            for invalid_email in self.INVALID_MAILS:
                _rich_client_data = self._rich_client_data()
                cd = SalesManagoClientData(**_rich_client_data)
                cd.email = invalid_email

    def test_owner_validated_on_create(self):
        with self.assertRaises(ValueError):
            for invalid_email in self.INVALID_MAILS:
                SalesManagoClientData(email=self.VALID_MAIL, owner=invalid_email)
    
    def test_owner_validated_on_change(self):
        with self.assertRaises(ValueError):
            for invalid_email in self.INVALID_MAILS:
                _rich_client_data = self._rich_client_data()
                cd = SalesManagoClientData(**_rich_client_data)
                cd.owner = invalid_email

    def test_create_rich_client_creation(self):
        rcd = self._rich_client_data()
        rich_client = SalesManagoClientData(**rcd)

        for key, value in rcd.items():
            self.assertEqual(getattr(rich_client, key), value)

    def test_create_rich_client_with_invalid_birthday_type(self):
        _rich_client_data = self._rich_client_data()
        _rich_client_data['birthday'] = '20200101'

        with self.assertRaises(TypeError):
            SalesManagoClientData(**_rich_client_data)
    
    def test_change_birthday_to_invalid_type(self):
        _rich_client_data = self._rich_client_data()

        with self.assertRaises(TypeError):
            cd = SalesManagoClientData(**_rich_client_data)
            cd.birthday = '20200101'

    def test_birthday_converter(self):
        self.assertEqual(self.richClientClass.birthDateConverted, self.rcd['birthday'].strftime('%Y%m%d'))

    def test_birthday_converter_no_birthday(self):
        self.assertEqual(self.clientClass.birthDateConverted, None)

    def test_newEmail_validated_on_create(self):
        _rich_client_data = self._rich_client_data()
        with self.assertRaises(ValueError):
            for invalid_email in self.INVALID_MAILS:
                _rich_client_data['newEmail'] = invalid_email
                SalesManagoClientData(**_rich_client_data)

    def test_state_values_on_creation(self):
        with self.assertRaises(ValueError):
            _rich_client_data = self._rich_client_data()
            _rich_client_data['state'] = 'ASDASDA'
            cd = SalesManagoClientData(**_rich_client_data)

    def test_state_values_on_change(self):
        with self.assertRaises(ValueError):
            _rich_client_data = self._rich_client_data()
            cd = SalesManagoClientData(**_rich_client_data)
            cd.state = 'ASDASDA'

    def test_tags_add(self):
        self.clientClass.add_tag('read')
        self.assertIn('read', self.clientClass.tags)

    def test_tags_remove(self):
        self.clientClass.add_tag('read')
        self.clientClass.remove_tag('read')
        self.assertNotIn('read', self.clientClass.tags)
    
    def test_tags_direct_creation(self):
        _rich_client_data = self._rich_client_data(fields=['email','owner'])
        _rich_client_data['tags'] = gen_list_of_strings(10)
        cd = SalesManagoClientData(**_rich_client_data)
        self.assertEqual(cd.tags, _rich_client_data['tags'].copy())
    
    def test_tags_direct_creation_invalid_type(self):
        _rich_client_data = self._rich_client_data(fields=['email','owner'])
        _rich_client_data['tags'] = gen_dict(10)
        with self.assertRaises(TypeError):
            cd = SalesManagoClientData(**_rich_client_data)


    def test_removeTags_add(self):
        self.clientClass.add_removeTags('read')
        self.assertIn('read', self.clientClass.removeTags)

    def test_removeTags_remove(self):
        self.clientClass.add_removeTags('read')
        self.clientClass.remove_removeTags('read')
        self.assertNotIn('read', self.clientClass.removeTags)
    
    def test_removeTags_direct_creation(self):
        _rich_client_data = self._rich_client_data(fields=['email','owner'])
        _rich_client_data['removeTags'] = gen_list_of_strings(10)
        cd = SalesManagoClientData(**_rich_client_data)
        self.assertEqual(cd.removeTags, _rich_client_data['removeTags'].copy())
    
    def test_removeTags_direct_creation_invalid_type(self):
        _rich_client_data = self._rich_client_data(fields=['email','owner'])
        _rich_client_data['removeTags'] = gen_dict(10)
        with self.assertRaises(TypeError):
            cd = SalesManagoClientData(**_rich_client_data)

    def test_properties_add(self):
        self.clientClass.add_property('read', 'not')
        self.assertIn('read', self.clientClass.properties)
        self.assertEqual('not', self.clientClass.properties['read'])

    def test_properties_remove(self):
        self.clientClass.add_property('read', 'not')
        self.clientClass.remove_property('read')
        self.assertNotIn('read', self.clientClass.properties)

    def test_properties_direct_creation(self):
        _rich_client_data = self._rich_client_data(fields=['email','owner'])
        _rich_client_data['properties'] = gen_dict(10)
        cd = SalesManagoClientData(**_rich_client_data)
        self.assertEqual(cd.properties, _rich_client_data['properties'].copy())

    def test_properties_direct_creation_invalid_type(self):
        _rich_client_data = self._rich_client_data(fields=['email','owner'])
        _rich_client_data['properties'] = gen_list_of_strings(10)
        with self.assertRaises(TypeError):
            cd = SalesManagoClientData(**_rich_client_data)

