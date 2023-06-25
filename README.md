# Todo List REST API with Authentication

This is a README file for a Todo List REST API with authentication. The API allows users to create and manage todo lists, create and update todo items, mark items as completed, delete items from a list, delete the entire list, and edit both items and lists.

## Getting Started

These instructions will guide you on how to set up and use the Todo List REST API on your local machine.

### Prerequisites

To run the API, you'll need the following installed on your machine:

- Python 3.11 or higher
- pipenv
- postgresql

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/todo-list-api.git
   ```

## Project setup
1. Navigate to the project directory:
   ```
   cd todo-list-api
   ```
2. Activate a virtual environment & install dependencies
   ```bash
   mkdir .venv && pipenv shell;
   pipenv install;

   ```
3. Set up the environment variables:
  ```
    Create a .env file in the root directory of the project.
    DEBUG=True
    SECRET_KEY='secret for the django project'
    DATABASE_URL=The connection URI for your postgres database.
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'apikey'
    EMAIL_HOST_PASSWORD = 'your key'
    EMAIL_PORT = 465
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL='prefereed email'
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
```
4. Start the server
```bash
    ./manage.py runserver

The API should now be running on http://localhost:8000/
```

5. Stop the server with `Ctrl+C`  and Create a test admin user
```
    ./manage.py createsuperuser
```

6. Restart the server and log into the admin interface
  ```
     http://localhost:8000/admin
  ```

## API Endpoints

## Authentication

### Register a User
```
URL: /auth/users/register
Method: POST
Request Body:
email: User's email address.
password: User's password.
Response:
email: The registered user's email.
token: An authentication token.
```
### Login
```
URL: /auth/login/user/
Method: POST
Request Body:
email: User's email address.
password: User's password.
Response:
msg: Success message.
token: An authentication token.
```

## Todo Lists
```
Create a Todo List
URL: /todos/lists/new-list/
Method: POST
Request Headers:
Authorization: Bearer token obtained during authentication.
Request Body:
title: Name of the todo list.

Response:
list: The created todo list object.
```
## Get All Todo Lists
```
URL: /lists
Method: GET
Request Headers:
Authorization: Bearer token obtained during authentication.
Response:
lists: An array of todo list objects.
```

## Get a Todo List
```
URL: /lists/:id
Method: GET
Request Headers:
Authorization: Bearer token obtained during authentication.
Response:
list: The requested todo list object.
Update a Todo List
URL: /lists/:id
Method: PUT
Request Headers:
Authorization: Bearer token obtained during authentication.
Request Body:
name: Updated name of the todo list.
Response:
list: The updated todo list object.
```

## Delete a Todo List
```
URL: /lists/:id
Method: DELETE
Request Headers:
Authorization: Bearer token obtained during authentication.
```
**Response:


### Check out the API

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/5140285-0cd4883f-4de8-4d6f-bbaf-f17268854a16?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D5140285-0cd4883f-4de8-4d6f-bbaf-f17268854a16%26entityType%3Dcollection%26workspaceId%3D7d07eb9f-ea3b-4c80-8843-fd704d8fb744)
