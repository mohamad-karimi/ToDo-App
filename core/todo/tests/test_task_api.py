import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from todo.models import Todo
from django.contrib.auth.models import Permission

User = get_user_model()


@pytest.fixture
def common_user():
    user = User.objects.create_user(username="test", email="test@gmail.com", password="@1234567")
    return user

@pytest.fixture
def user_permission(common_user):
    permission = Permission.objects.get(
        codename="add_post",
        content_type__app_label="blog",
    )

    create_user = common_user.user_permissions.add(permission)

    return create_user

@pytest.mark.django_db
class TestPostApi():
    client = APIClient()

    def test_get_post_api_response_status_401(self):
        url = reverse("todo:api-v1:task-list",)
        response = self.client.get(url)

        assert response.status_code == 401

    def test_create_post_response_status_401(self):
        url = reverse("todo:api-v1:task-list")

        data = {
            "title": "pytest"
        }

        response = self.client.post(url, data)

        assert response.status_code == 401

    def test_get_post_api_response_status_200(self, common_user):
        user = common_user
        self.client.force_authenticate(user=user)
        url = reverse("todo:api-v1:task-list",)
        response = self.client.get(url)

        assert response.status_code == 200

    def test_create_post_response_status_201(self, common_user):
        user = common_user
        self.client.force_authenticate(user=user)
        url = reverse("todo:api-v1:task-list")
        data = {
            "title": "pytest2"
        }

        response = self.client.post(url, data)

        assert response.status_code == 201

    def test_create_post_invalid_data_response_status_400(self):
        url = reverse("todo:api-v1:task-list")

        data = {
            "title": ""
        }

        response = self.client.post(url, data)

        assert response.status_code == 400

    def test_put_post_response_status_200(self, common_user):
        self.client.force_authenticate(user=common_user)

        todo = Todo.objects.create(
            user=common_user,
            title="test",
        )

        url = reverse(
            "todo:api-v1:task-detail",
            kwargs={"pk": todo.pk},
        )

        data = {
            "title": "updated test",
        }

        response = self.client.put(url, data)

        assert response.status_code == 200

    def test_put_post_response_status_400(self, common_user):
        self.client.force_authenticate(user=common_user)

        todo = Todo.objects.create(
            user=common_user,
            title="test",
        )

        url = reverse(
            "todo:api-v1:task-detail",
            kwargs={"pk": todo.pk},
        )

        data = {
            "title": "",
        }

        response = self.client.put(url, data)

        assert response.status_code == 400


    def test_delete_post_response_status_200(self, common_user):
        self.client.force_authenticate(user=common_user)

        todo = Todo.objects.create(
            user=common_user,
            title="test",
        )

        url = reverse(
            "todo:api-v1:task-detail",
            kwargs={"pk": todo.pk},
        )

        response = self.client.delete(url)

        assert response.status_code == 204