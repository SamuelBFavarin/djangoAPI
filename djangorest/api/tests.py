from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from .models import User
from .models import Salary


class ModelTestCase(TestCase):

    def setUp(self):

        # User values
        self.user_name = "Ronaldinho"
        self.user_cpf = "01542964067"
        self.date_birth = "1985-02-23T18:15:00Z"

        self.user = User(name=self.user_name,
                         cpf=self.user_cpf,
                         date_birth=self.date_birth)

        # Salary values
        self.salary_value = 45000
        self.salary_discount = 1000
        self.salary_user = self.user

    def test_model_can_create_a_user(self):
        old_count = User.objects.count()
        self.user.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_salary(self):

        self.user.save()

        self.salary = Salary(value=self.salary_value,
                             discount=self.salary_discount,
                             user=self.salary_user)

        old_count = Salary.objects.count()
        self.salary.save()
        new_count = Salary.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user_data = {'name': 'Ronaldinho',
                          'cpf': '01542964067',
                          'date_birth': '1985-02-23T18:15:00Z',
                          'salaries': []}

        self.response = self.client.post(
            reverse('create'),
            self.user_data,
            format="json")

        user = User.objects.get()

        self.salary_data = {'value': '40000',
                            'discount': '1000',
                            'user': user.id}

        self.response_post_salary = self.client.post(
            reverse('salary_create'),
            self.salary_data,
            format="json")

    def test_api_can_create_a_user(self):

        self.assertEqual(self.response.status_code,
                         status.HTTP_201_CREATED)

    def test_api_can_get_a_user(self):

        user = User.objects.get()

        response = self.client.get(
            reverse('details',
                    kwargs={'pk': user.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertContains(response, user)

    def test_api_can_update_user(self):

        change_user = {'name': 'Ronaldo Fenomeno',
                       'cpf': '03328801090',
                       'date_birth': '1986-02-23T18:15:00Z',
                       'salaries': []}

        user = User.objects.get()

        res = self.client.put(
            reverse('details', kwargs={'pk': user.id}),
            change_user, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_create_a_salary(self):

        self.assertEqual(self.response_post_salary.status_code,
                         status.HTTP_201_CREATED)

    def test_api_can_get_a_salary(self):

        salary = Salary.objects.get()

        response = self.client.get(
            reverse('salary_details',
                    kwargs={'pk': salary.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, salary)

    def test_api_can_update_salary(self):

        user = User.objects.get()
        salary = Salary.objects.get()

        change_salary = {'value': '40000',
                         'discount': '1000',
                         'user': user.id}

        res = self.client.put(
            reverse('salary_details', kwargs={'pk': salary.id}),
            change_salary, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_avg_value(self):

        user = User.objects.get()

        self.salary_data = {'value': '20000',
                            'discount': '2000',
                            'user': user.id}

        self.response_post_salary = self.client.post(
            reverse('salary_create'),
            self.salary_data,
            format="json")

        user_updated = User.objects.get()

        avg_salary_validated = 30000

        self.assertEqual(user_updated.avg_salary, avg_salary_validated)

    def test_api_avg_discount(self):
        user = User.objects.get()

        self.salary_data = {'value': '40000',
                            'discount': '3000',
                            'user': user.id}

        self.response_post_salary = self.client.post(
            reverse('salary_create'),
            self.salary_data,
            format="json")

        user_updated = User.objects.get()

        avg_discount_validated = 2000

        self.assertEqual(user_updated.avg_discount, avg_discount_validated)

    def test_api_bigger_salary(self):
        user = User.objects.get()

        self.salary_data = {'value': '80000',
                            'discount': '1000',
                            'user': user.id}

        self.response_post_salary = self.client.post(
            reverse('salary_create'),
            self.salary_data,
            format="json")

        user_updated = User.objects.get()

        bigger_value_validated = 80000

        self.assertEqual(user_updated.bigger_salary, bigger_value_validated)

    def test_api_lower_salary(self):
        user = User.objects.get()

        self.salary_data = {'value': '1000',
                            'discount': '100',
                            'user': user.id}

        self.response_post_salary = self.client.post(
            reverse('salary_create'),
            self.salary_data,
            format="json")

        user_updated = User.objects.get()

        lower_value_validated = 1000

        self.assertEqual(user_updated.lower_salary, lower_value_validated)

    def test_api_can_delete_salary(self):

        salary = Salary.objects.get()

        response = self.client.delete(
            reverse('salary_details', kwargs={'pk': salary.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code,
                          status.HTTP_204_NO_CONTENT)

    def test_api_can_delete_user(self):

        user = User.objects.get()

        response = self.client.delete(
            reverse('details', kwargs={'pk': user.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code,
                          status.HTTP_204_NO_CONTENT)
