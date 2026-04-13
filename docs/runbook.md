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

## Admin category creation

- `POST /categories` requires an `Authorization` token header
- The backend looks up the user by token
- Only users with `is_admin = true` can create categories
- Duplicate category names are rejected
- Non-admin users receive a `403 Admin access required` response

## Post creation

- `POST /posts` requires an `Authorization` token header
- The backend resolves the logged-in user from the token
- A valid `category_id` must exist before a post can be created
- Required fields are `title`, `content`, and `category_id`
- Each post is stored with `user_id`, `category_id`, and `created_at`
## Admin category update and delete

- `PUT /categories/<id>` requires an admin token in the `Authorization` header
- `DELETE /categories/<id>` also requires an admin token
- Invalid or missing tokens are rejected
- Non-admin users receive `403 Admin access required`
- Updating a category checks for duplicate names
- Deleting a category currently works if the category exists and no additional post rule has been added yet

## Public post reading

- `GET /posts` returns all posts publicly
- `GET /posts/<id>` returns one post publicly
- Responses include nested author and category information
- Missing post ids return `404 Post not found`
- No authentication is required for reading posts


