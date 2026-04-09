# Runbook

## Project purpose
A desktop GUI blogging app backed by a Flask JSON API and PostgreSQL database.

## Architecture
Tkinter GUI → Flask API → SQLAlchemy PostgreSQL

## Main files
- `backend.py` → backend API
- `frontend.py` → desktop GUI

## Main rules
- Anyone can register
- Passwords are stored as hashes
- Email is auto-generated
- Login uses a uuid4 token
- Admin users manage categories
- Logged-in users create posts
- Posts are immutable after creation
- Anyone can read posts and categories

## Data model

### User
- id
- first_name
- last_name
- email
- password_hash
- token
- is_admin

### Category
- id
- name

### Post
- id
- title
- content
- user_id
- category_id
- created_at

## Relationships
- One user can create many posts
- One category can contain many posts
- One post belongs to one user
- One post belongs to one category

## Environment variables

This project uses a `.env` file to store the database connection string.

Example:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost/blogging_app

## Login flow

- The user logs in with generated email and password
- The backend verifies the hashed password
- On successful login, the backend generates a UUID token
- The token is stored on the user record
- Protected routes will use this token to identify the logged-in user

## Categories

- Categories are stored in the `categories` table
- Categories are publicly readable through `GET /categories`
- At this stage, category management routes are not yet added


