# backend/tests/test_issues_api.py
import unittest
import json
from datetime import datetime, timezone
from backend.tests.base import BaseTestCase
from backend.models import Issue, db # Import your model and db

class TestIssueAPI(BaseTestCase):

    def test_create_issue(self):
        iso_time = datetime.now(timezone.utc).isoformat()
        response = self.app.post('/api/v1/issues',
                                 data=json.dumps({
                                     'title': 'Test Issue',
                                     'description': 'This is a test issue.',
                                     'location': 'Test Location',
                                     'system_affected': 'Test System',
                                     'occurrence_time': iso_time,
                                     'consequence': 'Test Consequence',
                                     'responsible_user_id': 1,
                                     'responsible_department_id': 1,
                                     'reporter_user_id': 2,
                                     'reporter_department_id': 2
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201, f"Response data: {response.data.decode()}")
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Issue')
        self.assertTrue('issue_id' in data)
        # Check if it's in the DB
        issue = Issue.query.get(data['issue_id'])
        self.assertIsNotNone(issue)

    def test_get_all_issues(self):
        # Create a couple of issues first
        iso_time1 = datetime.now(timezone.utc).isoformat()
        # Ensure occurrence_time is a datetime object for the model
        occurrence_time1 = datetime.fromisoformat(iso_time1.replace('Z', '+00:00'))
        occurrence_time2 = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)

        issue1 = Issue(title='Issue 1', occurrence_time=occurrence_time1)
        issue2 = Issue(title='Issue 2', occurrence_time=occurrence_time2)
        db.session.add_all([issue1, issue2])
        db.session.commit()

        response = self.app.get('/api/v1/issues')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], 'Issue 1')

    def test_get_single_issue(self):
        occurrence_time = datetime.now(timezone.utc)
        issue = Issue(title='Single Issue', occurrence_time=occurrence_time)
        db.session.add(issue)
        db.session.commit()

        response = self.app.get(f'/api/v1/issues/{issue.issue_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Single Issue')

    def test_get_single_issue_not_found(self):
        response = self.app.get('/api/v1/issues/999')
        self.assertEqual(response.status_code, 404)

    def test_update_issue(self):
        occurrence_time = datetime.now(timezone.utc)
        issue = Issue(title='Update Me', occurrence_time=occurrence_time)
        db.session.add(issue)
        db.session.commit()

        response = self.app.put(f'/api/v1/issues/{issue.issue_id}',
                                data=json.dumps({'title': 'Updated Title'}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200, f"Response data: {response.data.decode()}")
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Title')
        updated_issue = Issue.query.get(issue.issue_id)
        self.assertEqual(updated_issue.title, 'Updated Title')

    def test_update_issue_not_found(self):
        response = self.app.put('/api/v1/issues/999',
                                data=json.dumps({'title': 'Updated Title'}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)


    def test_delete_issue(self):
        occurrence_time = datetime.now(timezone.utc)
        issue = Issue(title='Delete Me', occurrence_time=occurrence_time)
        db.session.add(issue)
        db.session.commit()

        response = self.app.delete(f'/api/v1/issues/{issue.issue_id}')
        self.assertEqual(response.status_code, 204)
        deleted_issue = Issue.query.get(issue.issue_id)
        self.assertIsNone(deleted_issue)

    def test_delete_issue_not_found(self):
        response = self.app.delete('/api/v1/issues/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
