import pytest
from django.urls import reverse
from rest_framework import status

from tasks.models import Task
from tasks.tests.factories import TaskFactory
from users.tests.factories import UserFactory


class TestTaskGenericViewSet:
    list_action_url = reverse('api:tasks:tasks-list')
    detail_url = 'api:tasks:tasks-detail'

    @pytest.fixture
    def task(self):
        return TaskFactory()

    @pytest.fixture
    def task_for_authenticated_user(self, user):
        return TaskFactory(created_by=user)

    @pytest.fixture
    def valid_payload(self):
        return {
            'name': 'test_task',
            'description': 'test_description',
        }

    @pytest.fixture
    def invalid_payload(self):
        return {
            'is_done': 'abracadabra',
        }

    def test_list_action_succeed_for_unauthenticated_user(self, api_client, user):
        objects_count_for_unauthenticated = 5
        TaskFactory.create_batch(objects_count_for_unauthenticated, created_by=None)
        task_created_by_authenticated_user = TaskFactory(created_by=user)
        response = api_client.get(self.list_action_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == objects_count_for_unauthenticated
        for item in response.data:
            assert item['name'] is not None
            assert item['description'] is not None
            assert item['is_done'] is not None
            assert item['created_at'] is not None
            assert item['id'] != task_created_by_authenticated_user.id

    def test_list_action_succeed_for_authenticated_user(self, api_client, user):
        objects_count_for_authenticated = 5
        TaskFactory.create_batch(objects_count_for_authenticated, created_by=user)
        _task_created_by_unauthenticated_user = TaskFactory()
        other_user = UserFactory()
        task_created_by_other_authenticated_user = TaskFactory(created_by=other_user)
        api_client.force_authenticate(user=user)
        response = api_client.get(self.list_action_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == objects_count_for_authenticated + 1
        for item in response.data:
            assert item['name'] is not None
            assert item['description'] is not None
            assert item['is_done'] is not None
            assert item['created_at'] is not None
            assert item['id'] != task_created_by_other_authenticated_user.id

    def test_create_action_succeed_for_unauthenticated_user(self, api_client, valid_payload):
        assert Task.objects.count() == 0

        response = api_client.post(self.list_action_url, valid_payload)
        assert response.status_code == status.HTTP_201_CREATED

        instance = Task.objects.first()
        assert instance
        assert instance.name == valid_payload['name']
        assert instance.description == valid_payload['description']
        assert instance.is_done is False
        assert instance.created_by is None
        assert instance.created_at is not None

    def test_create_action_failed_for_unauthenticated_user(self, api_client, invalid_payload):
        assert Task.objects.count() == 0

        response = api_client.post(self.list_action_url, invalid_payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert Task.objects.count() == 0

    def test_create_action_succeed_for_authenticated_user(self, api_client, user, valid_payload):
        assert Task.objects.count() == 0

        api_client.force_authenticate(user)
        response = api_client.post(self.list_action_url, valid_payload)
        assert response.status_code == status.HTTP_201_CREATED

        instance = Task.objects.first()
        assert instance
        assert instance.name == valid_payload['name']
        assert instance.description == valid_payload['description']
        assert instance.is_done is False
        assert instance.created_by == user
        assert instance.created_at is not None

    def test_create_action_failed_for_authenticated_user(self, api_client, user, invalid_payload):
        assert Task.objects.count() == 0

        api_client.force_authenticate(user)
        response = api_client.post(self.list_action_url, invalid_payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert Task.objects.count() == 0

    def test_update_action_succeed_for_unauthenticated_user(self, api_client, valid_payload, task):
        detail_action_url = reverse(self.detail_url, args=(task.id,))
        response = api_client.patch(detail_action_url, valid_payload)
        assert response.status_code == status.HTTP_200_OK

        task.refresh_from_db()
        assert task.name == valid_payload['name']
        assert task.description == valid_payload['description']

    def test_update_action_failed_for_unauthenticated_user(
            self, api_client, valid_payload, task_for_authenticated_user
    ):
        detail_action_url = reverse(self.detail_url, args=(task_for_authenticated_user.id,))
        response = api_client.patch(detail_action_url, valid_payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_action_succeed_for_authenticated_user(
            self, api_client, valid_payload, task_for_authenticated_user, user
    ):
        detail_action_url = reverse(self.detail_url, args=(task_for_authenticated_user.id,))
        api_client.force_authenticate(user=user)
        response = api_client.patch(detail_action_url, valid_payload)
        assert response.status_code == status.HTTP_200_OK

        task_for_authenticated_user.refresh_from_db()
        assert task_for_authenticated_user.name == valid_payload['name']
        assert task_for_authenticated_user.description == valid_payload['description']

    def test_update_action_failed_for_authenticated_user(
            self, api_client, invalid_payload, task_for_authenticated_user, user
    ):
        detail_action_url = reverse(self.detail_url, args=(task_for_authenticated_user.id,))
        api_client.force_authenticate(user=user)
        response = api_client.patch(detail_action_url, invalid_payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_action_succeed_for_unauthenticated_user(self, api_client, task):
        detail_action_url = reverse(self.detail_url, args=(task.id,))
        response = api_client.get(detail_action_url)
        assert response.status_code == status.HTTP_200_OK

        assert response.data['id'] == task.id
        assert response.data['name'] == task.name
        assert response.data['description'] == task.description
        assert response.data['is_done'] == task.is_done

    def test_retrieve_action_failed_for_unauthenticated_user(self, api_client, task_for_authenticated_user):
        detail_action_url = reverse(self.detail_url, args=(task_for_authenticated_user.id,))
        response = api_client.get(detail_action_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_action_succeed_for_authenticated_user(self, api_client, task_for_authenticated_user, user):
        detail_action_url = reverse(self.detail_url, args=(task_for_authenticated_user.id,))
        api_client.force_authenticate(user=user)
        response = api_client.get(detail_action_url)
        assert response.status_code == status.HTTP_200_OK

        assert response.data['id'] == task_for_authenticated_user.id
        assert response.data['name'] == task_for_authenticated_user.name
        assert response.data['description'] == task_for_authenticated_user.description
        assert response.data['is_done'] == task_for_authenticated_user.is_done

    def test_retrieve_action_failed_for_authenticated_user(self, api_client, task_for_authenticated_user, user):
        detail_action_url = reverse(self.detail_url, args=(task_for_authenticated_user.id,))
        another_user = UserFactory()
        api_client.force_authenticate(user=another_user)
        response = api_client.get(detail_action_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_action_succeed_for_unauthenticated_user(self, api_client, task):
        assert Task.objects.exists()

        detail_action_url = reverse(self.detail_url, args=(task.id,))
        response = api_client.delete(detail_action_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Task.objects.exists()

    def test_delete_action_failed_for_unauthenticated_user(self, api_client, task_for_authenticated_user):
        assert Task.objects.exists()

        detail_action_url = reverse(self.detail_url, args=(task_for_authenticated_user.id,))
        response = api_client.delete(detail_action_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert Task.objects.exists()

    def test_delete_action_succeed_for_authenticated_user(self, api_client, task_for_authenticated_user, user):
        assert Task.objects.exists()

        detail_action_url = reverse(self.detail_url, args=(task_for_authenticated_user.id,))
        api_client.force_authenticate(user=user)
        response = api_client.delete(detail_action_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Task.objects.exists()

    def test_delete_action_failed_for_authenticated_user(self, api_client, task_for_authenticated_user, user):
        assert Task.objects.exists()

        detail_action_url = reverse(self.detail_url, args=(task_for_authenticated_user.id,))
        another_user = UserFactory()
        api_client.force_authenticate(user=another_user)

        response = api_client.delete(detail_action_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert Task.objects.exists()

    @pytest.mark.parametrize('is_done', [True, False])
    def test_filter_by_is_done(self, is_done, api_client):
        expected_task = TaskFactory(is_done=is_done)
        TaskFactory(is_done=not is_done)

        response = api_client.get(self.list_action_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        response = api_client.get(self.list_action_url, data={'is_done': is_done})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == expected_task.id

    def test_order_by_created_at(self, api_client):
        task_1 = TaskFactory()
        task_2 = TaskFactory()

        response = api_client.get(self.list_action_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['id'] == task_2.id
        assert response.data[1]['id'] == task_1.id

        response = api_client.get(self.list_action_url, data={'order_by': 'created_at'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['id'] == task_1.id
        assert response.data[1]['id'] == task_2.id

        response = api_client.get(self.list_action_url, data={'order_by': '-created_at'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['id'] == task_2.id
        assert response.data[1]['id'] == task_1.id

    def search_by_name(self, api_client):
        task_1 = TaskFactory(name='task_1')
        task_2 = TaskFactory(name='task_2')

        response = api_client.get(self.list_action_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        response = api_client.get(self.list_action_url, data={'search': task_1.name})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == task_1.id

        response = api_client.get(self.list_action_url, data={'search': task_2.name})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == task_2.id

        response = api_client.get(self.list_action_url, data={'search': 'abracadabra'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

        response = api_client.get(self.list_action_url, data={'search': 'task'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
