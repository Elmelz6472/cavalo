from django.test import TestCase
from .models import Client
from decimal import Decimal



class ClientModelTestCase(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            name='Test Client',
            phonenumber='123456789',
            location='Test Location',
            email='test@example.com',
            hourly_rate=10.0,
        )

    def test_client_creation(self):
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.first().name, 'Test Client')
        self.assertEqual(Client.objects.first().phonenumber, '123456789')
        self.assertEqual(Client.objects.first().location, 'Test Location')
        self.assertEqual(Client.objects.first().email, 'test@example.com')
        self.assertEqual(Client.objects.first().hourly_rate, 10.0)

    def test_client_string_representation(self):
        self.assertEqual(str(self.client), 'Test Client')

    def test_client_name_max_length(self):
        max_length = self.client._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_client_phonenumber_blank(self):
        blank = self.client._meta.get_field('phonenumber').blank
        self.assertTrue(blank)

    def test_client_location_max_length(self):
        max_length = self.client._meta.get_field('location').max_length
        self.assertEqual(max_length, 255)

    def test_client_email_max_length(self):
        max_length = self.client._meta.get_field('email').max_length
        self.assertEqual(max_length, 255)

    def test_client_email_valid(self):
        email_valid = self.client._meta.get_field('email').validators[0](self.client.email)
        self.assertIsNone(email_valid)

    def test_client_hourly_rate_default_value(self):
        default_value = self.client._meta.get_field('hourly_rate').default
        self.assertEqual(default_value, 0.00)

    def test_client_hourly_rate_decimal_places(self):
        decimal_places = self.client._meta.get_field('hourly_rate').decimal_places
        self.assertEqual(decimal_places, 2)

    def test_client_hourly_rate_max_digits(self):
        max_digits = self.client._meta.get_field('hourly_rate').max_digits
        self.assertEqual(max_digits, 10)

    def test_client_hourly_rate_positive(self):
        hourly_rate = self.client.hourly_rate
        self.assertGreater(hourly_rate, 0)

    def test_client_hourly_rate_rounding(self):
        client = Client.objects.create(
            name='Rounding Client',
            phonenumber='987654321',
            location='Rounding Location',
            email='rounding@example.com',
            hourly_rate=12.345,
        )
        self.assertAlmostEqual(client.hourly_rate, 12.35, places=2)
