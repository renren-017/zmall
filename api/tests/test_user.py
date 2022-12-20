from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class UserTest(TestCase):

    def test_user_creation(self):
        data = {
            'email': 'sample@gmail.com',
            'first_name': 'first',
            'last_name': 'last',
            'password': 'strongpass123'
        }
        response = self.client.post(reverse('api-register'), data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
