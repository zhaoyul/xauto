from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTests(APITestCase):
    def test_register(self):
        """
        Ensure user can register.
        """
        url = reverse('profiles-register')
        data = {'name': 'test',
                'user': {'full_name': 'test user',
                         'email': 'test@example.com',
                         'password_1': 'test',
                         'password_2': 'test',
                        },
                'username_available': "Available"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.has_key('token'))