**API Design for Issue Management**

**Base URL:** `/api/v1`

**Issues Endpoints**

*   **`POST /issues`**: Create a new issue.
    *   Request Body: JSON object (fields: `title`, `description`, `location`, `system_affected`, `occurrence_time`, `consequence`, `responsible_user_id`, `responsible_department_id`, `reporter_user_id`, `reporter_department_id`).
    *   Response (201 Created): JSON object of the created issue.
*   **`GET /issues`**: Get all issues.
    *   Response (200 OK): JSON array of issue objects.
*   **`GET /issues/<issue_id>`**: Get a specific issue.
    *   Response (200 OK): JSON object of the issue.
    *   Response (404 Not Found).
*   **`PUT /issues/<issue_id>`**: Update an issue.
    *   Request Body: JSON object with fields to update.
    *   Response (200 OK): JSON object of the updated issue.
    *   Response (404 Not Found).
*   **`DELETE /issues/<issue_id>`**: Delete an issue.
    *   Response (204 No Content).
    *   Response (404 Not Found).

**Discussions Endpoints**

*   **`POST /issues/<issue_id>/discussions`**: Add a discussion.
    *   Request Body: JSON object (fields: `user_id`, `discussion_time`, `location`, `content`, `conclusion`).
    *   Response (201 Created): JSON object of the created discussion.
    *   Response (404 Not Found: if issue_id is invalid).
*   **`GET /issues/<issue_id>/discussions`**: Get all discussions for an issue.
    *   Response (200 OK): JSON array of discussion objects.
    *   Response (404 Not Found: if issue_id is invalid).

**Solutions Endpoints**

*   **`POST /issues/<issue_id>/solution`**: Add/Update a solution.
    *   Request Body: JSON object (fields: `description`, `estimated_resolve_deadline`, `assigned_user_id`, `assigned_department_id`).
    *   Response (201 Created / 200 OK): JSON object of the solution.
    *   Response (404 Not Found: if issue_id is invalid).
*   **`GET /issues/<issue_id>/solution`**: Get the solution for an issue.
    *   Response (200 OK): JSON object of the solution.
    *   Response (404 Not Found: if issue_id or solution is invalid).
*   **`DELETE /issues/<issue_id>/solution`**: Delete the solution.
    *   Response (204 No Content).
    *   Response (404 Not Found: if issue_id or solution is invalid).
