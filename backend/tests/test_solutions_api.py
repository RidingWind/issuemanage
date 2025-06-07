# backend/tests/test_solutions_api.py
import unittest
import json
from datetime import datetime, date, timezone
from backend.tests.base import BaseTestCase
from backend.models import Issue, Solution, db

class TestSolutionAPI(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.occurrence_time_obj = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        self.test_issue = Issue(title='Issue for Solutions',
                                occurrence_time=self.occurrence_time_obj)
        db.session.add(self.test_issue)
        db.session.commit()
        self.issue_id = self.test_issue.issue_id

    def test_create_solution_for_issue(self):
        resolve_deadline_iso = date(2024, 12, 31).isoformat()
        response = self.app.post(f'/api/v1/issues/{self.issue_id}/solution',
                                 data=json.dumps({
                                     'description': 'This is the solution.',
                                     'estimated_resolve_deadline': resolve_deadline_iso,
                                     'assigned_user_id': 1,
                                     'assigned_department_id': 1
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201, f"Response data: {response.data.decode()}")
        data = json.loads(response.data)
        self.assertEqual(data['description'], 'This is the solution.')
        self.assertTrue('solution_id' in data)
        # Check DB
        solution = Solution.query.filter_by(issue_id=self.issue_id).first() # Solution is unique per issue_id
        self.assertIsNotNone(solution)
        self.assertEqual(solution.description, 'This is the solution.')


    def test_update_existing_solution(self):
        # Create initial solution
        initial_deadline = date(2024,1,1)
        sol = Solution(issue_id=self.issue_id, description='Initial Solution', estimated_resolve_deadline=initial_deadline)
        db.session.add(sol)
        db.session.commit()
        original_solution_id = sol.solution_id

        updated_deadline_iso = date(2024,2,2).isoformat()
        response = self.app.post(f'/api/v1/issues/{self.issue_id}/solution', # POST acts as create/update
                                 data=json.dumps({
                                     'description': 'Updated Solution',
                                     'estimated_resolve_deadline': updated_deadline_iso
                                     }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200, f"Response data: {response.data.decode()}") # Should be 200 for update
        data = json.loads(response.data)
        self.assertEqual(data['description'], 'Updated Solution')
        # Check DB (using db.session.get for modern SQLAlchemy)
        updated_solution = db.session.get(Solution, original_solution_id)
        self.assertIsNotNone(updated_solution)
        self.assertEqual(updated_solution.description, 'Updated Solution')
        self.assertEqual(updated_solution.estimated_resolve_deadline, date(2024,2,2))


    def test_create_solution_for_nonexistent_issue(self):
        resolve_deadline_iso = date(2024, 12, 31).isoformat()
        response = self.app.post('/api/v1/issues/999/solution',
                                 data=json.dumps({
                                     'description': 'Test Solution',
                                     'estimated_resolve_deadline': resolve_deadline_iso
                                     }), # Provide required fields
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_solution_for_issue(self):
        resolve_deadline = date(2024,1,1)
        sol = Solution(issue_id=self.issue_id, description='The Solution', estimated_resolve_deadline=resolve_deadline)
        db.session.add(sol)
        db.session.commit()

        response = self.app.get(f'/api/v1/issues/{self.issue_id}/solution')
        self.assertEqual(response.status_code, 200, f"Response data: {response.data.decode()}")
        data = json.loads(response.data)
        self.assertEqual(data['description'], 'The Solution')

    def test_get_solution_for_issue_with_no_solution(self):
        response = self.app.get(f'/api/v1/issues/{self.issue_id}/solution')
        self.assertEqual(response.status_code, 404)

    def test_get_solution_for_nonexistent_issue(self):
        response = self.app.get('/api/v1/issues/999/solution')
        self.assertEqual(response.status_code, 404)

    def test_delete_solution_for_issue(self):
        resolve_deadline = date(2024,1,1)
        sol = Solution(issue_id=self.issue_id, description='To Be Deleted', estimated_resolve_deadline=resolve_deadline)
        db.session.add(sol)
        db.session.commit()
        solution_id = sol.solution_id # Get ID before deletion

        response = self.app.delete(f'/api/v1/issues/{self.issue_id}/solution')
        self.assertEqual(response.status_code, 204, f"Response data: {response.data.decode()}")
        # Check DB (using db.session.get for modern SQLAlchemy)
        deleted_solution = db.session.get(Solution, solution_id)
        self.assertIsNone(deleted_solution)

    def test_delete_nonexistent_solution(self): # No solution for this issue
        response = self.app.delete(f'/api/v1/issues/{self.issue_id}/solution')
        self.assertEqual(response.status_code, 404)

    def test_delete_solution_for_nonexistent_issue(self):
        response = self.app.delete('/api/v1/issues/999/solution')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
