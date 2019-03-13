from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from workload.models import Workload, WallPhotoWrapper, WallPhoto, Location, Sketch


class MainWorkloadTest(APITestCase):

    def setUp(self):
        self.create_user()

    def create_user(self):
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
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + reg_response.data['access'])

    def create_workload(self):
        url = reverse('workload-list')
        data = {
            'requirements': 'I need some paint',
            'lng': 654.45,
            'lat': 875.12,
            'description': 'wucyfwe'
        }
        with open(r'C:\Users\gursk\projects\anyart_api\ananas.jpg', 'rb') as fp:
            data['photo'] = fp
            workload_response = self.client.post(url, data)
        return workload_response

    def test_1workload_endpoint(self):
        # test post
        workload_response = self.create_workload()

        self.assertEqual(workload_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workload.objects.count(), 1)
        self.assertEqual(WallPhotoWrapper.objects.count(), 1)
        self.assertEqual(WallPhoto.objects.count(), 1)
        self.assertEqual(Location.objects.count(), 1)

        # test get list
        url = reverse('workload-list')
        workload_response = self.client.get(url)
        self.assertEqual(workload_response.status_code, status.HTTP_200_OK)

        # test get retrieve
        url = reverse('workload-detail', kwargs={'pk': 1})
        workload_response = self.client.get(url)
        self.assertEqual(workload_response.status_code, status.HTTP_200_OK)

        workload_response = self.client.put(url)
        self.assertEqual(workload_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_2wall_photo_wrapper(self):
        self.create_workload()

        # test get list
        url = reverse('workload-wall_photo_wrapper-list', kwargs={'workload_pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test get retrieve
        url = reverse('workload-wall_photo_wrapper-detail', kwargs={'workload_pk': 2, 'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_3sketch(self):
        self.create_workload()

        # test post
        url = reverse('workload-sketch-list', kwargs={'workload_pk': Workload.objects.first().id})
        data = {
            'comment': 'This is my first sketch'
        }
        with open(r'C:\Users\gursk\projects\anyart_api\ananas.jpg', 'rb') as fp:
            data['sketch'] = fp
            sketch_response = self.client.post(url, data)
        self.assertEqual(sketch_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sketch.objects.count(), 1)
        self.assertEqual(Sketch.objects.first().workload_id, Workload.objects.first().id)

        # test get retrieve
        url = reverse('workload-sketch-detail', kwargs={'workload_pk': 3, 'pk': 1})
        sketch_get_response = self.client.get(url)
        self.assertEqual(sketch_get_response.status_code, status.HTTP_200_OK)

        # test get list
        url = reverse('workload-sketch-list', kwargs={'workload_pk': 3})
        sketch_response = self.client.get(url)
        self.assertEqual(sketch_response.status_code, status.HTTP_200_OK)

        # test put
        url = reverse('workload-sketch-detail', kwargs={'workload_pk': Workload.objects.first().id,
                                                        'pk': Sketch.objects.first().id})
        data = {
            'sketch_description': 'different_text',
        }
        sketch_response = self.client.put(url, data)
        self.assertEqual(sketch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sketch.objects.first().sketch_description, 'different_text')
