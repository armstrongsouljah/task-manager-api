# Todo List App REST API

The API allows users to create and manage todo lists, create and update todo items, mark items as completed, delete items from a list, delete the entire list, and edit both items and lists.

## Getting Started

These instructions will guide you on how to set up and use the Todo List REST API on your local machine.

### Prerequisites

To run the API, you'll need the following installed on your machine:

- Python 3.11
- pipenv
- postgresql
- redis
- celery
- Postman / Insomnia for testing the api.

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
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'your-email'
    EMAIL_HOST_PASSWORD = 'your-app-password' `set up an app password for your gmail`
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL='your-email'
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    ALLOWED_HOSTS=.localhost,localhost
```
4. Start the server
```bash
    ./manage.py runserver

The API should now be running on http://localhost:8000/
```

4.1. Start the celery worker in a separate terminal
```bash
     python -m celery -A todolist worker -l info

Celery should now be able to offload heavy tasks.
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
URL: auth/users/login/user/
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
URL: /todos/lists/
Method: GET
Request Headers:
Authorization: Bearer token obtained during authentication.
Response:
lists: An array of todo list objects.
```

## Update a Todo List
```
URL: /todos/lists/update/?short_code=shortcode
Method: PATCH
Request Headers:
Authorization: Bearer token obtained during authentication.
Response:
msg: Success or failure of updating a tod list.


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
URL: /todos/lists/delete-list/?pk=list_id
Method: DELETE
Request Headers:
Authorization: Bearer token obtained during authentication.
```
**Response:


## Todo List Items
```
Create a Todo List
URL: /todos/items/new-item/
Method: POST
Request Headers:
Authorization: Bearer token obtained during authentication.
Request Body:
name: Name of the tod item.
todo_list: pk of the list it should belong to

Response:
object: The created todo item object
```
## Get All Todo Items
```
URL: /todos/items/
Method: GET
Request Headers:
Authorization: Bearer token obtained during authentication.
Response:
lists: An array of todo item objects.
```

## Mark a todo item complete
```
URL: /todos/items/complete/?pk=1
Method: PATCH
Request Headers:
Authorization: Bearer token obtained during authentication.
RequestBody:
  is_completed: true or false "to mark on unmark an item"
Response:
msg: Success or failure of updating a tod list.


Mark Entire Todo list completed
URL: /todos/lists/update/?short_code=D1IJZ7vA
Method: PUT
Request Headers:
Authorization: Bearer token obtained during authentication.
Request Body:
is_completed: Boolean to mark completed
QueryParams:
short_code: unique identifier for list.
Response:
dict: Success or failure message.
```

## Delete a Todo Item
```
URL: /todos/items/delete-item/?pk=5&todo_list=2
Method: DELETE
Request Headers:
Authorization: Bearer token obtained during authentication.
QueryParams:
pk: id of todo item
todo_list: pk of the list from which you're removing the item.
```
**Response:


### Check out the API

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/5140285-0cd4883f-4de8-4d6f-bbaf-f17268854a16?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D5140285-0cd4883f-4de8-4d6f-bbaf-f17268854a16%26entityType%3Dcollection%26workspaceId%3D7d07eb9f-ea3b-4c80-8843-fd704d8fb744)
