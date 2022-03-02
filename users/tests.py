from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from users.models import User


class UserTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_registration = reverse('users:registration')
        self.user_data = {
            'first_name': 'Наталья', 'last_name': 'Сидоренко', 'username': 'Nata',
            'email': '1@mail.ru', 'password1': '12345678q+', 'password2': '12345678q+'
        }

    def test_user_registration_GET(self):
        response = self.client.get(self.url_registration)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_POST(self):

        response = self.client.post(self.url_registration, self.user_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())

    def test_user_registration_POST_already_exists(self):
        data = {
            'first_name': 'Наталья', 'last_name': 'Сидоренко', 'username': 'Nata',
            'email': '1@mail.ru', 'password1': '12345678q_', 'password2': '12345678q_'
        }

        self.client.post(self.url_registration, self.user_data)
        response = self.client.post(self.url_registration, data)

        response_form = response.context['form']
        self.assertFalse(response_form.is_valid())
        self.assertEqual(response_form.errors['username'][0], 'Пользователь с таким именем уже существует.')
        self.assertEqual(User.objects.count(), 1)




