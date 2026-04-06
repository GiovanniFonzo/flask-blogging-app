# Runbook

## Project purpose
A desktop GUI blogging app backed by a Flask JSON API and MySQL database.

## Architecture
Tkinter GUI → Flask API → SQLAlchemy → MySQL

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


