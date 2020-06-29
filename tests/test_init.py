import unittest

'''
class FirstTestClass(unittest.TestCase):

    
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.x = X()

    def tearDown(self) -> None:
        pass

    def test_upper(self):
        self.assertEqual('rubiks code'.upper(), 'RUBIKS CODE')
        with self.assertRaises(ValueError):
            Temperature(celsius=-274)
    def test_permission_add(self):
        self.user.add_permission('read')
        self.assertIn('read', self.user.permission)

    def test_permission_remove(self):
        self.user.add_permission('read')
        self.user.remove_permission('read')
        self.assertNotIn('read', self.user.permission)

    def test_date_of_birth_in_utc(self):
        self.assertEqual(self.user.date_of_birth.tzinfo, timezone.utc)

    def test_date_of_birth_not_in_utc(self):
        with self.assertRaises(ValueError):
            now = datetime.now()
            user = User(first_name='Jan', last_name='Twardowski', date_of_birth=now)
            self.assertEqual(user.date_of_birth.tzinfo, timezone.utc)

    
    
'''
