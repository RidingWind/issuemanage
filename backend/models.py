# backend/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Issue(db.Model):
    __tablename__ = 'issues'
    issue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.Text)
    system_affected = db.Column(db.Text)
    occurrence_time = db.Column(db.DateTime, nullable=False)
    consequence = db.Column(db.Text)
    responsible_user_id = db.Column(db.Integer)
    responsible_department_id = db.Column(db.Integer)
    reporter_user_id = db.Column(db.Integer)
    reporter_department_id = db.Column(db.Integer)
    creation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Text, default='Open')

    discussions = db.relationship('Discussion', backref='issue', lazy=True, cascade="all, delete-orphan")
    solution = db.relationship('Solution', backref='issue', uselist=False, lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'issue_id': self.issue_id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'system_affected': self.system_affected,
            'occurrence_time': self.occurrence_time.isoformat() + 'Z' if self.occurrence_time else None,
            'consequence': self.consequence,
            'responsible_user_id': self.responsible_user_id,
            'responsible_department_id': self.responsible_department_id,
            'reporter_user_id': self.reporter_user_id,
            'reporter_department_id': self.reporter_department_id,
            'creation_timestamp': self.creation_timestamp.isoformat() + 'Z' if self.creation_timestamp else None,
            'status': self.status
        }

class Discussion(db.Model):
    __tablename__ = 'discussions'
    discussion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.issue_id'), nullable=False)
    user_id = db.Column(db.Integer)
    discussion_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    conclusion = db.Column(db.Text)
    creation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'discussion_id': self.discussion_id,
            'issue_id': self.issue_id,
            'user_id': self.user_id,
            'discussion_time': self.discussion_time.isoformat() + 'Z' if self.discussion_time else None,
            'location': self.location,
            'content': self.content,
            'conclusion': self.conclusion,
            'creation_timestamp': self.creation_timestamp.isoformat() + 'Z' if self.creation_timestamp else None
        }

class Solution(db.Model):
    __tablename__ = 'solutions'
    solution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.issue_id'), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    estimated_resolve_deadline = db.Column(db.Date)
    assigned_user_id = db.Column(db.Integer)
    assigned_department_id = db.Column(db.Integer)
    creation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'solution_id': self.solution_id,
            'issue_id': self.issue_id,
            'description': self.description,
            'estimated_resolve_deadline': self.estimated_resolve_deadline.isoformat() if self.estimated_resolve_deadline else None,
            'assigned_user_id': self.assigned_user_id,
            'assigned_department_id': self.assigned_department_id,
            'creation_timestamp': self.creation_timestamp.isoformat() + 'Z' if self.creation_timestamp else None,
            'updated_timestamp': self.updated_timestamp.isoformat() + 'Z' if self.updated_timestamp else None
        }
