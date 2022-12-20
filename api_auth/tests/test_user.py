from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class UserTest(TestCase):

    def setUp(self):
        pass

    def test_user_creation(self):
        data = {
            'email': 'sample@gmail.com',
            'first_name': 'first',
            'last_name': 'last',
            'password': 'strongpass123'
        }
        print('THIS IS FIRST TEST')
        response = self.client.post(reverse('api-register'), data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_token(self):
        data = {
            'email': 'sample@gmail.com',
            'first_name': 'first',
            'last_name': 'last',
            'password': 'strongpass123'
        }

        print('THIS IS SECOND TEST')
        response = self.client.post(reverse('api-register'), data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'email': 'sample@gmail.com',
            'password': 'strongpass123'
        }
        response = self.client.post(reverse('api-token-obtain'), data, format='json', content_type='application/json')
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
