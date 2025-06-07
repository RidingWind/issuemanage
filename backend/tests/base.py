# backend/tests/base.py
import unittest
from backend.app import app as _app # Import your Flask app instance
from backend.models import db as _db # Import your SQLAlchemy db instance

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        _app.config['TESTING'] = True
        # Consider using a different DB for testing if possible, e.g., SQLite in-memory or a separate test PG DB
        # For this subtask, we'll assume the main dev DB URI is okay for now, or that it can be overridden
        _app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://swebot:password@localhost:5432/issue_tracker_test_db'
        self.app = _app.test_client() # Create a test client
        self.app_context = _app.app_context()
        self.app_context.push() # Push an application context
        _db.create_all() # Create all database tables

    def tearDown(self):
        _db.session.remove()
        _db.drop_all()
        self.app_context.pop()
