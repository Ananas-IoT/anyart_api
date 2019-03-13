from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from authorization.models import BasicUserProfile, ArtistUserProfile


class DummyTest(APITestCase):

    def test_root(self):
        url ='/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class AuthorizationTest(APITestCase):

    def test_auth(self):
        url = reverse('user_create')
        data = {
            'username': 'username',
            'password': 'password',
            'first_name': 'John',
            'last_name': 'Silver',
            'email': 'mail@gmail.com',
            'rights': 'artist'
        }

        reg_response = self.client.post(url, data, format='json')

        user_model = get_user_model()

        # test user creation
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_model.objects.count(), 1)
        self.assertEqual(user_model.objects.filter(username='username').get().first_name, 'John')

        # test profile creation
        self.assertEqual(ArtistUserProfile.objects.filter(owner_id=1).count(), 1)
        self.assertEqual(BasicUserProfile.objects.filter(owner_id=1).count(), 0)

        # test rights field validation
        data = {
            'username': 'username1',
            'password': 'password1',
            'first_name': 'John',
            'last_name': 'Silver',
            'email': 'mail1@gmail.com',
            'rights': 'randomstring'
        }

        db_response = self.client.post(url, data, format='json')

        self.assertEqual(db_response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('token_obtain_pair')

        data = {
            'username': 'username',
            'password': 'password'
        }

        log_response = self.client.post(url, data, format='json')

        self.assertEqual(log_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(log_response.data.keys()), ['refresh', 'access'])