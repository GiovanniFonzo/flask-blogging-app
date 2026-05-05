# Project Bullets

- Built a Python blogging application using Flask, SQLAlchemy, PostgreSQL, and Tkinter with clear API/frontend separation.
- Designed a relational data model for users, categories, and posts with one-to-many relationships, foreign keys, and role-based content rules.
- Implemented secure registration and login using hashed passwords and UUID token-based authentication.
- Developed protected category management routes with administrator-only create, update, and delete operations.
- Built authenticated post creation linked to users and categories through SQLAlchemy relationships and PostgreSQL persistence.
- Exposed public JSON endpoints for category listing, post listing, and post detail views.
- Enforced immutable post rules by supporting create/read flows only and intentionally omitting post update/delete operations.
- Developed a Tkinter desktop client for registration, login, post creation, category/post listing, and admin category management.
- Improved the Create Post workflow by loading categories dynamically from the Flask API into a dropdown instead of requiring manual category ID entry.
- Added role-aware frontend behavior with admin controls disabled for non-admin users and a logout workflow that clears token-based session state and resets the interface.

