import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class UserTest(TestCase):

    @staticmethod
    def get_object(obj=User):
        return obj.objects.first()

    def setUp(self):
        user = User.objects.create(
            email="sample@gmail.com",
            first_name="User",
            last_name="User",
            is_active=True
        )
        user.set_password("strongpass123")
        user.save()

    def test_user_creation(self):
        data = {
            'email': 'sample2@gmail.com',
            'first_name': 'second',
            'last_name': 'last',
            'password': 'strongpass12345'
        }

        start = time.time()
        response = self.client.post(reverse('api-register'), data, format='json', content_type='application/json')
        end = time.time()

        self.assertLess(end - start, 0.5)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['is_active'], False)

    def test_get_token(self):

        data = {
            'email': 'sample@gmail.com',
            'password': 'strongpass123'
        }

        start = time.time()
        response = self.client.post(reverse('api-token-obtain'), data, format='json', content_type='application/json')
        end = time.time()

        self.assertLess(end - start, 0.5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.get_object().is_active, True)

    def test_get_token_invalid_credentials(self):

        data = {
            'email': 'nonexistent@gmail.com',
            'password': 'nonex123'
        }

        start = time.time()
        response = self.client.post(reverse('api-token-obtain'), data, format='json', content_type='application/json')
        end = time.time()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertLess(start - end, 0.03)