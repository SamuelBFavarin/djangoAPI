from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from .models import User
from .models import Salary


class ModelTestCase(TestCase):
    """This class defines the test suite for the user model."""

    def setUp(self):
        """Define the test client and other test variables."""

        self.user_name = "Ronaldinho"
        self.user_cpf = "01542964067"
        self.date_birth = "1985-02-23T18:15:00Z"
        self.user = User(name=self.user_name,
                         cpf=self.user_cpf,
                         date_birth=self.date_birth)

    def test_model_can_create_a_user(self):
        """Test the user model can create a user."""
        old_count = User.objects.count()
        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user_data = {'name': 'Ronaldinho',
                          'cpf': '01542964067',
                          'date_birth': '1985-02-23T18:15:00Z'}
        self.response = self.client.post(
            reverse('create'),
            self.user_data,
            format="json")

    def test_api_can_create_a_user(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_user(self):
        """Test the api can get a given user."""
        user = User.objects.get()

        response = self.client.get(
            reverse('details',
                    kwargs={'pk': user.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, user)

    def test_api_can_update_user(self):
        """Test the api can update a given user."""
        change_user = {'name': 'Ronaldo Fenomeno',
                       'cpf': '03328801090',
                       'date_birth': '1986-02-23T18:15:00Z'}
        user = User.objects.get()
        res = self.client.put(
            reverse('details', kwargs={'pk': user.id}),
            change_user, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_user(self):
        """Test the api can delete a user."""
        user = User.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': user.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
