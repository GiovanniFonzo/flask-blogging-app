# Blogging App

A Python blogging application with:

- Flask backend API
- SQLAlchemy ORM
- MySQL database
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

Tkinter GUI → Flask API → SQLAlchemy → MySQL

