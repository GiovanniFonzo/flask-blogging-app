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

