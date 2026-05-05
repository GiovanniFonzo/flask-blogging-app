# Blogging App

A Python blogging application with:

- Flask backend API
- SQLAlchemy ORM
- PostgreSQL database
- Tkinter desktop frontend

## Main rules

- Anyone can register
- Passwords must be stored as hashes
- Email is auto-generated as `first_name.last_name@google.com`
- Login uses a `uuid4` token
- Admin users can manage categories
- Logged-in users can create posts
- Posts cannot be edited or deleted once created
- Anyone can read posts and categories

## Architecture

Tkinter GUI → Flask API → SQLAlchemy → PostgreSQL

## Main entities

### User
A registered person in the system. A user has a first name, last name, generated email, hashed password, login token, and admin status.

### Category
A grouping for blog posts. Categories are managed by admin users.

### Post
A blog post created by a logged-in user. Every post belongs to one category and cannot be edited or deleted after creation.

## Data model

### User fields
- `id`
- `first_name`
- `last_name`
- `email`
- `password_hash`
- `token`
- `is_admin`

### Category fields
- `id`
- `name`

### Post fields
- `id`
- `title`
- `content`
- `user_id`
- `category_id`
- `created_at`

## Relationships

- One user can create many posts
- One category can contain many posts
- One post belongs to one user
- One post belongs to one category

## Business rules mapped to data

- A user must have a first name, last name, and password
- A user's email is generated automatically from first name and last name
- A user's password is stored as a hash
- A user may or may not be an admin
- A post must belong to exactly one user
- A post must belong to exactly one category
- Categories are created, updated, and deleted only by admin users
- Posts are immutable after creation
- Posts and categories can be read by anyone

## Simple schema view

### User
- `id`
- `first_name`
- `last_name`
- `email`
- `password_hash`
- `token`
- `is_admin`

### Category
- `id`
- `name`

### Post
- `id`
- `title`
- `content`
- `user_id -> User.id`
- `category_id -> Category.id`
- `created_at`

## Backend features

- Users can log in with email and password
- Successful login returns a UUID token used for authenticated actions
- Anyone can read the list of categories through the API
- Admin users can create categories through a protected API route
- Admin users can update and delete categories through protected API routes
- Logged-in users can create posts that belong to a category
- Anyone can read all posts or a single post without logging in
- Posts are immutable after creation and cannot be edited or deleted

## Backend API

### Auth
- `POST /register`
- `POST /login`

### Categories
- `GET /categories`
- `POST /categories`
- `PUT /categories/<id>`
- `DELETE /categories/<id>`

### Posts
- `GET /posts`
- `GET /posts/<id>`
- `POST /posts`

## Frontend

The project includes a Tkinter desktop frontend that communicates with the Flask backend API.

### Current frontend features
- Register a user
- Log in a user
- View categories
- View posts
- Create a post when logged in
- The Tkinter frontend includes admin category management tools for authorized users
- The Create Post form loads categories dynamically and shows them in a dropdown
- Admin category buttons are role-aware in the Tkinter frontend
- The Tkinter frontend includes a logout workflow that resets the current session state

## Frontend design

The frontend is a class-based Tkinter app where one `BloggingAppGUI` object manages the window, stores app state, builds reusable UI sections, handles button workflows, and communicates with the Flask backend through a shared API helper.

### Frontend flow

Tk root window  
→ `BloggingAppGUI` object  
→ static shell (title, status, buttons, output)  
→ dynamic workflows (register, login, create post, list data)  
→ API helper sends requests to Flask  
→ backend returns JSON  
→ frontend updates output, status, and messages

## Architecture overview

This project is split into three layers:

```text
Tkinter GUI (frontend)
        │
        │ HTTP requests with JSON
        ▼
Flask API (backend)
        │
        │ SQLAlchemy queries
        ▼
PostgreSQL database
```

The Tkinter frontend is the only interface the user interacts with. It sends JSON requests to the Flask backend, which handles business logic, interacts with the database through SQLAlchemy, and returns JSON responses back to the GUI.

## Frontend and backend design

The frontend is built as a class-based Tkinter application. One `BloggingAppGUI` object manages the window, stores app state such as the logged-in user and token, builds the layout, and handles workflows like register, login, and create post.

The backend is built as a Flask API. The Flask app object registers route functions for each HTTP endpoint, while model classes such as `User`, `Post`, and `Category` define the database structure and relationships.

In short, the frontend uses one persistent GUI object because it manages screen state during the session, while the backend uses a Flask app object plus route handlers because it processes requests one at a time.

## Local configuration note

The Flask API runs on port `5050` in this project to avoid a local port conflict on this machine.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/GiovanniFonzo/flask-blogging-app.git
cd flask-blogging-app
```

### 2. Create and activate the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the `.env` file

Create a `.env` file in the project root with:

```env
DATABASE_URL=postgresql+psycopg2://your_username:your_password@localhost/blogging_app
```

### 5. Start the backend

```bash
python backend.py
```

The backend runs on:

`http://127.0.0.1:5050`

### 6. Start the frontend

Open a new terminal:

```bash
cd flask-blogging-app
source venv/bin/activate
python frontend.py
```

## Example workflow

1. Register a user
2. Log in with the generated email and password
3. If logged in as admin, manage categories
4. Create a post as a logged-in user
5. Read categories and posts publicly through the GUI

## Current status

The project has been tested end to end across:
- registration
- login
- logout
- role-aware admin controls
- category create, update, and delete
- post creation
- public post and category reading
- immutable post behavior

## Future improvements

- Hide admin controls entirely for non-admin users instead of only disabling them
- Refresh category and post views automatically after create/update/delete actions
- Add more polished form validation messages
- Add automated tests and GitHub Actions CI
- Add category selection improvements or post detail screens in the GUI

