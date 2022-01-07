from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserInteractionAPITestCase(APITestCase):

    def test_create_user_interaction_api(self):
        data = {"user_id": 1, "content_id": 1, "is_like": True, "is_read": False}
        response = self.client.post(reverse('interaction-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)