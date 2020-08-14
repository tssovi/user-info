import json
import random
from rest_framework import status
from django.test import TestCase, Client

from users.models import Users
from users.serializers import UsersSerializer

from users.test_data.data_seed import insert_data


# initialize the APIClient app
client = Client()


class GetAllKeyValueTest(TestCase):
    """ Test module for GET all key value API """

    def setUp(self):
        data = insert_data
        s_users, e_users = Users.objects.insert_user_data(data)

        self.valid_insert_payload = [{
            "first_name": "Test",
            "last_name": "Parent 11",
            "address": "Test Address",
            "street": "Test Street",
            "city": "Test City",
            "state": "Test State",
            "zip_code": "1234",
            "user_type": "parent",
            "parent_id": ""
        }]

        self.invalid_insert_payload = [{
            "first_name": "Test",
            "last_name": "Child 1",
            "user_type": "child",
            "parent_id": "ABCD1234"
        }]

        self.invalid_update_payload = [{
            "user_id": "ABCD1234",
            "first_name": "Test",
            "last_name": "Parent Update 1",
            "address": "Test Update Address",
            "street": "Test Update Street",
            "city": "Test Update City",
            "state": "Test Update State",
            "zip_code": "9876",
            "user_type": "parent",
            "parent_id": ""
        }]

    def test_get_all_key_values(self):
        # get API response
        response = client.get('/user-info/api/v1/user/')

        # get data from db
        user_data = Users.objects.get_all_users()
        serializer = UsersSerializer(user_data, many=True)
        res_len = len(response.data['data'])
        ser_len = len(serializer.data)
        self.assertEqual(response.data['data'], serializer.data)
        self.assertEqual(res_len, ser_len)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_user_id_for_test(self):
        user_data = Users.objects.get_all_users()
        serializer = UsersSerializer(user_data, many=True)
        user_data = serializer.data
        user_ids = []
        for data in user_data:
            user_ids.append(data['user_id'])
        random_ids = random.sample(user_ids, 2)
        user_id_1 = random_ids[0]
        user_id_2 = random_ids[1]

        return user_id_1, user_id_2

    def test_get_with_valid_user_id(self):
        user_id_1, user_id_2 = self.get_user_id_for_test()

        # get API response
        response = client.get('/user-info/api/v1/user/?user_ids={}'.format(user_id_1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get API response
        response = client.get('/user-info/api/v1/user/?user_ids={},{}'.format(user_id_1, user_id_2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_with_invalid_user_id(self):
        # get API response
        response = client.get('/user-info/api/v1/user/?user_ids=ABCD1234')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # get API response
        response = client.get('/user-info/api/v1/user/?user_ids=ABCD1234,EFGH5678')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_with_valid_data(self):
        data = json.dumps(self.valid_insert_payload)
        response = client.post(
            '/user-info/api/v1/user/',
            data=json.dumps(self.valid_insert_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_invalid_data(self):
        response = client.post(
            '/user-info/api/v1/user/',
            data=json.dumps(self.invalid_insert_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_with_valid_user_id(self):
        user_id_1, user_id_2 = self.get_user_id_for_test()

        valid_update_payload = [{
            "user_id": user_id_1,
            "first_name": "Test",
            "last_name": "Parent Update 1",
            "address": "Test Update Address",
            "street": "Test Update Street",
            "city": "Test Update City",
            "state": "Test Update State",
            "zip_code": "9876",
            "user_type": "parent",
            "parent_id": ""
        }]
        response = client.patch(
            '/user-info/api/v1/user/',
            data=json.dumps(valid_update_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_with_invalid_user_id(self):
        response = client.patch(
            '/user-info/api/v1/user/',
            data=json.dumps(self.invalid_update_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
