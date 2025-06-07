# backend/populate_sample_data.py
from datetime import datetime, timezone
from backend.app import app  # Import the Flask app instance
from backend.models import db, Issue  # Import db and Issue model

def populate():
    with app.app_context(): # Push an application context
        # Clear existing issues (optional, but good for repeatable script)
        # Issue.query.delete()
        # db.session.commit() # Not doing this here as init-db should handle clean slate

        print("Populating sample issues...")

        issue1_occurrence = datetime(2024, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
        issue1 = Issue(
            title="Frontend Login Button Not Working",
            description="The login button on the main page is unresponsive on Chrome.",
            location="Login Page",
            system_affected="WebApp v1.2",
            occurrence_time=issue1_occurrence,
            consequence="Users cannot log in.",
            reporter_user_id=101,
            status="Open"
        )

        issue2_occurrence = datetime(2024, 6, 2, 14, 30, 0, tzinfo=timezone.utc)
        issue2 = Issue(
            title="API Performance Degradation",
            description="The /api/v1/data endpoint is taking >5s to respond.",
            location="API Gateway",
            system_affected="Backend API Services",
            occurrence_time=issue2_occurrence,
            consequence="Slow response times for clients.",
            responsible_user_id=201,
            responsible_department_id=3,
            status="In Progress"
        )

        issue3_occurrence = datetime(2024, 5, 15, 9, 0, 0, tzinfo=timezone.utc)
        issue3 = Issue(
            title="Database Backup Failure",
            description="Nightly database backups have been failing since last Monday.",
            location="DB Server Rack 3",
            system_affected="PostgreSQL Main Cluster",
            occurrence_time=issue3_occurrence,
            consequence="Potential data loss if primary fails.",
            reporter_user_id=55,
            status="Closed"
        )

        db.session.add_all([issue1, issue2, issue3])
        db.session.commit()
        print(f"Added issue: {issue1.title} (ID: {issue1.issue_id})")
        print(f"Added issue: {issue2.title} (ID: {issue2.issue_id})")
        print(f"Added issue: {issue3.title} (ID: {issue3.issue_id})")
        print("Sample data populated.")

if __name__ == '__main__':
    populate()
