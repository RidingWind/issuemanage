// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';
import IssueList from './components/IssueList';

function App() {
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/v1/issues') // Proxied to backend
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setIssues(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching issues:", error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Issue Management</h1>
      </header>
      <main>
        {loading && <p>Loading issues...</p>}
        {error && <p>Error fetching issues: {error}</p>}
        {!loading && !error && <IssueList issues={issues} />}
      </main>
    </div>
  );
}

export default App;
