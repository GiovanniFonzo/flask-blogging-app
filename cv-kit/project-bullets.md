# Project Bullets

- Planned and scaffolded a Python blogging application using Flask, SQLAlchemy, PostgreSQL, and Tkinter with clear API/frontend separation.

- Designed a relational data model for users, categories, and posts with one-to-many relationships and role-based content rules.

- Implemented token-based login using password-hash verification and UUID authentication tokens stored against registered users.

- Added a category model and public JSON endpoint for listing content categories from PostgreSQL through Flask.

- Implemented admin-only category creation with token-based authentication, role checks, duplicate protection, and JSON API responses.

- Added administrator-only category update and delete routes with token validation, role checks, and category existence handling.

- Built authenticated post creation linked to users and categories using Flask, SQLAlchemy relationships, PostgreSQL foreign keys, and token-based authorization.

- Exposed public post list and detail endpoints with nested author and category data using SQLAlchemy relationships and JSON serialization.

- Enforced immutable post rules by exposing create/read routes only and intentionally omitting post update/delete operations at the backend level.

- Built a desktop blogging application with a Tkinter GUI client, Flask JSON API, SQLAlchemy, and PostgreSQL, implementing user registration, hashed-password authentication, UUID token-based login, admin-managed categories, post/category listing, and authenticated post creation.





