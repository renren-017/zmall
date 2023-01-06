from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class UserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            email="sample@gmail.com'",
            first_name="User",
            last_name="User",
            is_active=True
        )
        user.set_password("strongpass123")
        user.save()

    def setUp(self):
        pass

    def test_user_creation(self):
        data = {
            'email': 'sample@gmail.com',
            'first_name': 'first',
            'last_name': 'last',
            'password': 'strongpass123'
        }
        response = self.client.post(reverse('api-register'), data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_token(self):
        if User.objects.get(email='sample@gmail.com').is_active:
            print("USER IS ACTIVE")
        data = {
            'email': 'sample@gmail.com',
            'password': 'strongpass123'
        }
        response = self.client.post(reverse('api-token-obtain'), data, format='json', content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
