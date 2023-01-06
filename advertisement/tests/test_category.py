from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from time import time


from advertisement.models import Category, SubCategory

User = get_user_model()


class CategoryTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            email="user@example.com",
            first_name="User",
            last_name="User",
            is_active=True
        )
        user.set_password("cantrem21")
        Category.objects.create(
            title="Cat"
        )

    @staticmethod
    def get_object(obj=Category):
        return obj.objects.first()

    def setUp(self):
        user = self.get_object(obj=User)
        self.client.force_authenticate(user)

    def test_categories_get(self):
        start = time()
        response = self.client.get(reverse("category-list"), format='json')
        end = time()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertLess(end-start, 0.25)

    def test_category_post(self):
        data = {
            "title": "New Cat",
        }

        start = time()
        response = self.client.post(reverse("category-list"), data)
        end = time()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertLess(end-start, 0.009)

    def test_categories_post_unauthorized(self):
        self.client.logout()

        data = {
            "title": "New Cat",
        }

        start = time()
        response = self.client.post(reverse("category-list"), data=data)
        end = time()

        self.assertLess(end-start, 0.004)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_category_delete(self):
        cat = self.get_object()

        start = time()
        response = self.client.delete(reverse("category-detail", kwargs={"slug": cat.slug}))
        end = time()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Category.objects.count(), 0)
        self.assertLess(end - start, 0.25)


class SubCategoryTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            email="user@example.com",
            first_name="User",
            last_name="User",
            is_active=True
        )
        user.set_password("cantrem21")
        cat = Category.objects.create(
            title="Cat"
        )
        SubCategory.objects.create(
            title="SubCat",
            category=cat
        )

    @staticmethod
    def get_object(obj=SubCategory):
        return obj.objects.first()

    def setUp(self):
        user = self.get_object(obj=User)
        self.client.force_authenticate(user)

    def test_subcategories_get(self):
        start = time()
        response = self.client.get(reverse("sub-category-list"), format='json')
        end = time()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertLess(end-start, 0.25)

    def test_subcategory_post(self):
        cat = self.get_object(obj=Category)

        data = {
            "title": "New Cat",
            "category": cat.id
        }

        start = time()
        response = self.client.post(reverse("sub-category-list"), data)
        end = time()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertLess(end-start, 0.009)

    def test_subcategories_post_unauthorized(self):
        self.client.logout()

        cat = self.get_object(obj=Category)
        data = {
            "title": "New Cat",
            "category": cat.id
        }

        start = time()
        response = self.client.post(reverse("sub-category-list"), data=data)
        end = time()

        self.assertLess(end-start, 0.004)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


    def test_subcategory_delete(self):
        cat = self.get_object()

        start = time()
        response = self.client.delete(reverse("sub-category-detail", kwargs={"slug": cat.slug}))
        end = time()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertLess(end - start, 0.25)
