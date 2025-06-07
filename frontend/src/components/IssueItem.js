// frontend/src/components/IssueItem.js
import React from 'react';
import './IssueItem.css'; // We will create this

function IssueItem({ issue }) {
  return (
    <div className="issue-item">
      <h3>{issue.title}</h3>
      <p><strong>Status:</strong> {issue.status}</p>
      <p><strong>Reported:</strong> {new Date(issue.occurrence_time).toLocaleString()}</p>
    </div>
  );
}

export default IssueItem;
