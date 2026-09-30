from django.test import TestCase
from rest_framework.test import APIRequestFactory

from loganalyzerapi.models import LogMaster
from loganalyzerapi.views import LogMasterViewSet


class ProjectCreationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LogMasterViewSet.as_view({'post': 'create'})
        LogMaster.objects.create(
            creator='alice', project_name='Access logs', project_description='Existing',
        )

    def create_project(self, creator='alice', name='Access logs'):
        return self.view(self.factory.post('/logmaster/', {
            'creator': creator,
            'project_name': name,
            'project_description': 'New project',
        }, format='json'))

    def test_duplicate_is_rejected_without_creating_a_row(self):
        response = self.create_project()
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)
        self.assertEqual(LogMaster.objects.count(), 1)

    def test_other_account_can_use_same_name(self):
        self.assertEqual(self.create_project(creator='bob').status_code, 201)
        self.assertEqual(LogMaster.objects.count(), 2)

    def test_same_account_can_use_another_name(self):
        self.assertEqual(self.create_project(name='Other logs').status_code, 201)

    def test_surrounding_whitespace_does_not_bypass_duplicate_check(self):
        self.assertEqual(self.create_project(name=' Access logs ').status_code, 400)
        self.assertEqual(LogMaster.objects.count(), 1)
