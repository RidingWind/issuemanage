# backend/tests/test_discussions_api.py
import unittest
import json
from datetime import datetime, timezone
from backend.tests.base import BaseTestCase
from backend.models import Issue, Discussion, db

class TestDiscussionAPI(BaseTestCase):

    def setUp(self):
        super().setUp() # Call BaseTestCase.setUp()
        # Create a test issue
        # Use a fixed, parsable ISO string for occurrence_time in tests
        self.occurrence_time_obj = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        self.test_issue = Issue(title='Issue for Discussions',
                                occurrence_time=self.occurrence_time_obj)
        db.session.add(self.test_issue)
        db.session.commit()
        self.issue_id = self.test_issue.issue_id

    def test_create_discussion_for_issue(self):
        discussion_time_obj = datetime(2024, 1, 1, 13, 0, 0, tzinfo=timezone.utc)
        discussion_time_iso = discussion_time_obj.isoformat()
        response = self.app.post(f'/api/v1/issues/{self.issue_id}/discussions',
                                 data=json.dumps({
                                     'user_id': 1,
                                     'discussion_time': discussion_time_iso, # Send ISO string
                                     'location': 'Meeting Room',
                                     'content': 'This is a test discussion.',
                                     'conclusion': 'No conclusion yet.'
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201, f"Response data: {response.data.decode()}")
        data = json.loads(response.data)
        self.assertEqual(data['content'], 'This is a test discussion.')
        self.assertTrue('discussion_id' in data)
        # Check DB (using db.session.get for modern SQLAlchemy)
        discussion = db.session.get(Discussion, data['discussion_id'])
        self.assertIsNotNone(discussion)
        self.assertEqual(discussion.issue_id, self.issue_id)

    def test_create_discussion_for_nonexistent_issue(self):
        discussion_time_obj = datetime(2024, 1, 1, 13, 0, 0, tzinfo=timezone.utc)
        discussion_time_iso = discussion_time_obj.isoformat()
        response = self.app.post('/api/v1/issues/999/discussions',
                                 data=json.dumps({
                                     'user_id': 1,
                                     'discussion_time': discussion_time_iso,
                                     'location': 'Meeting Room',
                                     'content': 'This is a test discussion.',
                                     'conclusion': 'No conclusion yet.'
                                 }), # Provide all required fields for a valid request body
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_discussions_for_issue(self):
        dt1 = datetime(2024, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        dt2 = datetime(2024, 1, 1, 15, 0, 0, tzinfo=timezone.utc)
        disc1 = Discussion(issue_id=self.issue_id, user_id=1, discussion_time=dt1, content='Disc 1')
        disc2 = Discussion(issue_id=self.issue_id, user_id=2, discussion_time=dt2, content='Disc 2')
        db.session.add_all([disc1, disc2])
        db.session.commit()

        response = self.app.get(f'/api/v1/issues/{self.issue_id}/discussions')
        self.assertEqual(response.status_code, 200, f"Response data: {response.data.decode()}")
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        # Order might not be guaranteed, so check contents flexibly
        contents = {item['content'] for item in data}
        self.assertIn('Disc 1', contents)
        self.assertIn('Disc 2', contents)


    def test_get_discussions_for_issue_with_no_discussions(self):
        response = self.app.get(f'/api/v1/issues/{self.issue_id}/discussions')
        self.assertEqual(response.status_code, 200, f"Response data: {response.data.decode()}")
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    def test_get_discussions_for_nonexistent_issue(self):
        response = self.app.get('/api/v1/issues/999/discussions')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
