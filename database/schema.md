# Database Schema

## issues table

| Column                   | Data Type                  | Constraints                               |
| ------------------------ | -------------------------- | ----------------------------------------- |
| `issue_id`               | Auto-incrementing Integer  | Primary Key                               |
| `title`                  | Text                       | Not Null                                  |
| `description`            | Text                       |                                           |
| `location`               | Text                       |                                           |
| `system_affected`        | Text                       |                                           |
| `occurrence_time`        | Timestamp                  | Not Null                                  |
| `consequence`            | Text                       |                                           |
| `responsible_user_id`    | Integer                    |                                           |
| `responsible_department_id` | Integer                    |                                           |
| `reporter_user_id`       | Integer                    |                                           |
| `reporter_department_id` | Integer                    |                                           |
| `creation_timestamp`     | Timestamp                  | Default Current Timestamp                 |
| `status`                 | Text                       | Default 'Open'                            |

## discussions table

| Column                | Data Type                  | Constraints                               |
| --------------------- | -------------------------- | ----------------------------------------- |
| `discussion_id`       | Auto-incrementing Integer  | Primary Key                               |
| `issue_id`            | Integer                    | Foreign Key to issues table, Not Null     |
| `user_id`             | Integer                    |                                           |
| `discussion_time`     | Timestamp                  | Not Null                                  |
| `location`            | Text                       |                                           |
| `content`             | Text                       | Not Null                                  |
| `conclusion`          | Text                       |                                           |
| `creation_timestamp`  | Timestamp                  | Default Current Timestamp                 |

## solutions table

| Column                   | Data Type                  | Constraints                               |
| ------------------------ | -------------------------- | ----------------------------------------- |
| `solution_id`            | Auto-incrementing Integer  | Primary Key                               |
| `issue_id`               | Integer                    | Foreign Key to issues table, Not Null, Unique |
| `description`            | Text                       | Not Null                                  |
| `estimated_resolve_deadline` | Date                       |                                           |
| `assigned_user_id`       | Integer                    |                                           |
| `assigned_department_id` | Integer                    |                                           |
| `creation_timestamp`     | Timestamp                  | Default Current Timestamp                 |
