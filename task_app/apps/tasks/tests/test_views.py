from datetime import datetime

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
            'status': 'abracadabra',
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
            assert item['status'] is not None
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
            assert item['status'] is not None
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
        assert instance.status == Task.STATUS.to_do
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
        assert instance.status == Task.STATUS.to_do
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
        assert response.data['status'] == task.status

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
        assert response.data['status'] == task_for_authenticated_user.status

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

    @pytest.mark.parametrize(
        'query,length',
        (
            ({'status': Task.STATUS.done}, 1),
            ({'status': Task.STATUS.to_do}, 1),
            ({}, 2)
        )
    )
    def test_filter_by_status(self, query, length, api_client):
        TaskFactory(status=Task.STATUS.done)
        TaskFactory(status=Task.STATUS.to_do)

        response = api_client.get(self.list_action_url, data=query)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == length
        if query:
            assert response.data[0]['status'] == query['status']

    @pytest.mark.parametrize(
        'query,is_reverse',
        (
            ({'order_by': 'created_at'}, False),
            ({'order_by': '-created_at'}, True),
            ({}, True)
        )
    )
    def test_order_by_created_at(self, query, is_reverse, api_client):
        TaskFactory.create_batch(2)
        response = api_client.get(self.list_action_url, data=query)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data == sorted(
            response.data,
            key=lambda x: datetime.fromisoformat(x['created_at']),
            reverse=is_reverse
        )

    @pytest.mark.parametrize(
        'query,expected_result_cnt',
        (
            ({'search': 'abracadabra'}, 0),
            ({'search': 'task_1'}, 1),
            ({'search': 'task_2'}, 1),
            ({'search': ''}, 2),
            ({'search': 'task'}, 2),
            ({}, 2)
         )
    )
    def search_by_name(self, query, expected_result_cnt, api_client):
        TaskFactory(name='task_1')
        TaskFactory(name='task_2')

        response = api_client.get(self.list_action_url, data=query)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_result_cnt

        if expected_result_cnt == 1:
            assert response.data[0]['name'] == query['search']
