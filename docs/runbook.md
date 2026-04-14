# Runbook

## Project purpose
A desktop GUI blogging app backed by a Flask JSON API and PostgreSQL database.

## Architecture
Tkinter GUI → Flask API → SQLAlchemy → PostgreSQL

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

## Immutable posts

- Posts can be created through `POST /posts`
- Posts can be read through `GET /posts` and `GET /posts/<id>`
- Posts cannot be updated or deleted
- No `PUT` or `DELETE` routes are implemented for posts
- This business rule is enforced at the backend level

## Tkinter frontend

The frontend is a Tkinter desktop application that acts as a client for the Flask API.

### Current frontend features
- User registration form
- User login form
- Status label showing logged-in user
- Category listing
- Post listing
- Authenticated post creation

### Frontend auth state
- After login, the frontend stores the returned token in memory
- The frontend also stores the current user details
- Protected requests send the token in the `Authorization` header

### Frontend/backend separation
- Tkinter does not access PostgreSQL directly
- Tkinter only communicates with the Flask backend through HTTP requests
- Business rules are enforced by the backend, not only by the GUI

## Frontend mental model

The frontend is built as a class-based Tkinter application.

### Core structure

Tk root window  
→ `BloggingAppGUI` object  
→ static shell (title, status, buttons, output area)  
→ dynamic workflows (register, login, create post, list categories, list posts)  
→ shared API helper  
→ Flask backend  
→ JSON response  
→ GUI update

### App startup flow

1. Create the Tkinter root window
2. Create the `BloggingAppGUI` object
3. The object initializes app state such as token and current user
4. The object builds the static layout
5. `mainloop()` starts the GUI event loop

### User interaction flow

1. The user clicks a button
2. The matching GUI method runs
3. The method may build a form or call the backend
4. The backend returns a JSON response
5. The frontend updates the output area, status label, or popup message

### Design summary

The frontend is designed so that Tkinter handles interface state and user interaction, while Flask handles business rules, authentication, and database access.

## Runtime Flow

1. Start the Flask backend.
2. Start the Tkinter frontend.
3. Register or log in through the GUI.
4. The frontend sends JSON requests to the backend API.
5. The backend processes the request, interacts with the database, and returns JSON responses.
6. The frontend updates the GUI with the result.

## Validation Checklist

- Register a new user successfully
- Log in successfully and receive a token
- Create a category as an admin user
- Create a blog post as a logged-in user
- View categories without logging in
- View posts without logging in

## Troubleshooting

### Frontend cannot connect to backend
- Check that the Flask server is running
- Check that the API base URL in the frontend matches the backend address
- Check that the backend port is correct

### Database errors
- Check that PostgreSQL is running
- Check that the database name, username, and password are correct
- Check that the tables have been created

### Unauthorized or token errors
- Log in again to get a new token
- Make sure the frontend is sending the token in the request
- Check that protected routes require authentication correctly


