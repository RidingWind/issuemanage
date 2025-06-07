from flask import Flask, jsonify, request, Blueprint
from datetime import datetime, timezone # Added timezone
from .models import db, Issue, Discussion, Solution # Import models

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://swebot:password@localhost:5432/issue_tracker_db' # Use correct credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# API Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@app.route('/')
def hello():
    return "Issue Management API is running with SQLAlchemy!"

# --- Helper function to parse datetime strings ---
def parse_datetime_string(dt_str):
    if not dt_str:
        return None
    # Handles strings ending with 'Z' (UTC) or having timezone offset like +00:00
    if dt_str.endswith('Z'):
        dt_str = dt_str[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError: # Handle cases where fromisoformat might fail if no timezone info after removing Z
        return datetime.fromisoformat(dt_str + '+00:00')


# --- Issue Endpoints ---
@api_bp.route('/issues', methods=['POST'])
def create_issue():
    data = request.get_json()

    if not data or not data.get('title') or not data.get('occurrence_time'):
        return jsonify({"error": "Missing required fields: title and occurrence_time"}), 400

    occurrence_dt = parse_datetime_string(data.get('occurrence_time'))
    if not occurrence_dt:
         return jsonify({"error": "Invalid occurrence_time format"}), 400

    new_issue = Issue(
        title=data.get('title'),
        description=data.get('description'),
        location=data.get('location'),
        system_affected=data.get('system_affected'),
        occurrence_time=occurrence_dt,
        consequence=data.get('consequence'),
        responsible_user_id=data.get('responsible_user_id'),
        responsible_department_id=data.get('responsible_department_id'),
        reporter_user_id=data.get('reporter_user_id'),
        reporter_department_id=data.get('reporter_department_id'),
        status=data.get('status', 'Open')
        # creation_timestamp is handled by default in model
    )
    db.session.add(new_issue)
    db.session.commit()
    return jsonify(new_issue.to_dict()), 201

@api_bp.route('/issues', methods=['GET'])
def get_issues():
    issues = Issue.query.all()
    return jsonify([issue.to_dict() for issue in issues]), 200

@api_bp.route('/issues/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    issue = db.session.get(Issue, issue_id) # Use db.session.get for primary key lookups
    if issue:
        return jsonify(issue.to_dict()), 200
    return jsonify({"error": "Issue not found"}), 404

@api_bp.route('/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    issue = db.session.get(Issue, issue_id)
    if not issue:
        return jsonify({"error": "Issue not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400

    # Update fields if provided in request data
    for key, value in data.items():
        if key == 'occurrence_time':
            setattr(issue, key, parse_datetime_string(value))
        elif hasattr(issue, key) and key not in ['issue_id', 'creation_timestamp']:
            setattr(issue, key, value)

    db.session.commit()
    return jsonify(issue.to_dict()), 200

@api_bp.route('/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    issue = db.session.get(Issue, issue_id)
    if not issue:
        return jsonify({"error": "Issue not found"}), 404

    db.session.delete(issue)
    db.session.commit()
    return '', 204

# --- Placeholder/Modified Discussion Endpoints (to be fully updated later) ---
# For now, these will likely fail or not work as expected as discussions_db is removed.
# The subtask stated to focus on Issue CRUD first.
# These should be updated in a subsequent subtask.

@api_bp.route('/issues/<int:issue_id>/discussions', methods=['POST'])
def create_discussion_for_issue(issue_id):
    parent_issue = db.session.get(Issue, issue_id)
    if not parent_issue:
        return jsonify({"error": "Issue not found"}), 404

    data = request.get_json()
    if not data or not data.get('content') or not data.get('discussion_time'):
        return jsonify({"error": "Missing required fields: content and discussion_time"}), 400

    discussion_dt = parse_datetime_string(data.get('discussion_time'))
    if not discussion_dt:
        return jsonify({"error": "Invalid discussion_time format"}), 400

    new_discussion = Discussion(
        issue_id=parent_issue.issue_id, # or issue=parent_issue
        user_id=data.get('user_id'),
        discussion_time=discussion_dt,
        location=data.get('location'),
        content=data.get('content'),
        conclusion=data.get('conclusion')
        # creation_timestamp is handled by default
    )
    db.session.add(new_discussion)
    db.session.commit()
    return jsonify(new_discussion.to_dict()), 201

@api_bp.route('/issues/<int:issue_id>/discussions', methods=['GET'])
def get_discussions_for_issue(issue_id):
    parent_issue = db.session.get(Issue, issue_id)
    if not parent_issue:
        return jsonify({"error": "Issue not found"}), 404

    discussions = Discussion.query.filter_by(issue_id=issue_id).all()
    # Alternatively, could use parent_issue.discussions if lazy='dynamic' or already loaded
    return jsonify([discussion.to_dict() for discussion in discussions]), 200

# --- Solution Endpoints ---
@api_bp.route('/issues/<int:issue_id>/solution', methods=['POST'])
def add_or_update_solution_for_issue(issue_id):
    parent_issue = db.session.get(Issue, issue_id)
    if not parent_issue:
        return jsonify({"error": "Issue not found"}), 404

    data = request.get_json()
    if not data or not data.get('description'):
        return jsonify({"error": "Missing required field: description"}), 400

    existing_solution = Solution.query.filter_by(issue_id=issue_id).first()

    if existing_solution:
        # Update existing solution
        existing_solution.description = data.get('description', existing_solution.description)
        deadline_str = data.get('estimated_resolve_deadline')
        if deadline_str:
            existing_solution.estimated_resolve_deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        else:
            existing_solution.estimated_resolve_deadline = None # Allow clearing the deadline

        existing_solution.assigned_user_id = data.get('assigned_user_id', existing_solution.assigned_user_id)
        existing_solution.assigned_department_id = data.get('assigned_department_id', existing_solution.assigned_department_id)
        # updated_timestamp is handled by onupdate in model
        db.session.commit()
        return jsonify(existing_solution.to_dict()), 200
    else:
        # Create new solution
        deadline = None
        deadline_str = data.get('estimated_resolve_deadline')
        if deadline_str:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()

        new_solution = Solution(
            issue_id=parent_issue.issue_id, # or issue=parent_issue
            description=data.get('description'),
            estimated_resolve_deadline=deadline,
            assigned_user_id=data.get('assigned_user_id'),
            assigned_department_id=data.get('assigned_department_id')
            # creation_timestamp & updated_timestamp handled by default/onupdate
        )
        db.session.add(new_solution)
        db.session.commit()
        return jsonify(new_solution.to_dict()), 201

@api_bp.route('/issues/<int:issue_id>/solution', methods=['GET'])
def get_solution_for_issue(issue_id):
    parent_issue = db.session.get(Issue, issue_id)
    if not parent_issue:
        return jsonify({"error": "Issue not found"}), 404

    solution = Solution.query.filter_by(issue_id=issue_id).first()
    # Alternatively, parent_issue.solution if relationship is correctly set up and loaded
    if solution:
        return jsonify(solution.to_dict()), 200
    return jsonify({"error": "Solution not found for this issue"}), 404

@api_bp.route('/issues/<int:issue_id>/solution', methods=['DELETE'])
def delete_solution_for_issue(issue_id):
    parent_issue = db.session.get(Issue, issue_id)
    if not parent_issue:
        return jsonify({"error": "Issue not found"}), 404

    solution_to_delete = Solution.query.filter_by(issue_id=issue_id).first()
    if not solution_to_delete:
        return jsonify({"error": "Solution not found for this issue"}), 404

    db.session.delete(solution_to_delete)
    db.session.commit()
    return '', 204


# Register blueprint
app.register_blueprint(api_bp)

# CLI command to create DB tables
@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    # No need for app.app_context() here if using Flask 2.x+ with db.init_app
    # However, it's good practice if compatibility with older Flask is a concern
    # or if used outside of app context setup by Flask CLI for some reason.
    # For Flask-SQLAlchemy, db.create_all() needs an app context.
    # The CLI command itself runs within an app context.
    db.create_all()
    print('Initialized the database.')

if __name__ == '__main__':
    # Note: For production, use a WSGI server like Gunicorn or uWSGI
    app.run(debug=True, host='0.0.0.0', port=5000)
