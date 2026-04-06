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

Tkinter GUI → Flask API → SQLAlchemy → MySQL

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

User
- id
- first_name
- last_name
- email
- password_hash
- token
- is_admin

Category
- id
- name

Post
- id
- title
- content
- user_id -> User.id
- category_id -> Category.id
- created_at




