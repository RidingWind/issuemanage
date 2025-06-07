// frontend/src/components/IssueList.js
import React from 'react';
import IssueItem from './IssueItem'; // We will create this
import './IssueList.css'; // We will create this

function IssueList({ issues }) {
  if (!issues || issues.length === 0) {
    return <p>No issues to display.</p>;
  }

  return (
    <div className="issue-list">
      {issues.map(issue => (
        <IssueItem key={issue.issue_id} issue={issue} />
      ))}
    </div>
  );
}

export default IssueList;
