from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    token = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    
    posts = relationship("Post", back_populates="author")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    posts = relationship("Post", back_populates="category")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(2000), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")


Base.metadata.create_all(bind=engine)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    password = data.get("password")
    is_admin = data.get("is_admin", False)

    if not first_name or not last_name or not password:
        return jsonify({"error": "first_name, last_name, and password are required"}), 400

    email = f"{first_name.lower()}.{last_name.lower()}@google.com"
    password_hash = generate_password_hash(password)

    session = SessionLocal()

    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        session.close()
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
        is_admin=is_admin
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    session.close()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        }
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    session = SessionLocal()

    user = session.query(User).filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        session.close()
        return jsonify({"error": "Invalid email or password"}), 401

    user.token = str(uuid.uuid4())
    session.commit()
    session.refresh(user)
    session.close()

    return jsonify({
        "message": "Login successful",
        "token": user.token,
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }), 200


@app.route("/categories", methods=["GET"])
def get_categories():
    session = SessionLocal()
    categories = session.query(Category).all()

    result = []
    for category in categories:
        result.append({
            "id": category.id,
            "name": category.name
        })

    session.close()
    return jsonify(result), 200


@app.route("/categories", methods=["POST"])
def create_category():
    token = request.headers.get("Authorization")
    data = request.get_json()

    name = data.get("name") if data else None

    if not token:
        return jsonify({"error": "Authorization token is required"}), 401

    if not name:
        return jsonify({"error": "Category name is required"}), 400

    session = SessionLocal()

    user = session.query(User).filter_by(token=token).first()
    if not user:
        session.close()
        return jsonify({"error": "Invalid token"}), 401

    if not user.is_admin:
        session.close()
        return jsonify({"error": "Admin access required"}), 403

    existing_category = session.query(Category).filter_by(name=name).first()
    if existing_category:
        session.close()
        return jsonify({"error": "Category already exists"}), 400

    category = Category(name=name)
    session.add(category)
    session.commit()
    session.refresh(category)
    session.close()

    return jsonify({
        "message": "Category created successfully",
        "category": {
            "id": category.id,
            "name": category.name
        }
    }), 201


@app.route("/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    token = request.headers.get("Authorization")
    data = request.get_json()

    name = data.get("name") if data else None

    if not token:
        return jsonify({"error": "Authorization token is required"}), 401

    if not name:
        return jsonify({"error": "Category name is required"}), 400

    session = SessionLocal()

    user = session.query(User).filter_by(token=token).first()
    if not user:
        session.close()
        return jsonify({"error": "Invalid token"}), 401

    if not user.is_admin:
        session.close()
        return jsonify({"error": "Admin access required"}), 403

    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        session.close()
        return jsonify({"error": "Category not found"}), 404

    existing_category = session.query(Category).filter_by(name=name).first()
    if existing_category and existing_category.id != category_id:
        session.close()
        return jsonify({"error": "Category already exists"}), 400

    category.name = name
    session.commit()
    session.refresh(category)
    session.close()

    return jsonify({
        "message": "Category updated successfully",
        "category": {
            "id": category.id,
            "name": category.name
        }
    }), 200



@app.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Authorization token is required"}), 401

    session = SessionLocal()

    user = session.query(User).filter_by(token=token).first()
    if not user:
        session.close()
        return jsonify({"error": "Invalid token"}), 401

    if not user.is_admin:
        session.close()
        return jsonify({"error": "Admin access required"}), 403

    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        session.close()
        return jsonify({"error": "Category not found"}), 404

    session.delete(category)
    session.commit()
    session.close()

    return jsonify({"message": "Category deleted successfully"}), 200


@app.route("/posts", methods=["POST"])
def create_post():
    token = request.headers.get("Authorization")
    data = request.get_json()

    title = data.get("title") if data else None
    content = data.get("content") if data else None
    category_id = data.get("category_id") if data else None

    if not token:
        return jsonify({"error": "Authorization token is required"}), 401

    if not title or not content or not category_id:
        return jsonify({"error": "title, content, and category_id are required"}), 400

    session = SessionLocal()

    user = session.query(User).filter_by(token=token).first()
    if not user:
        session.close()
        return jsonify({"error": "Invalid token"}), 401

    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        session.close()
        return jsonify({"error": "Category not found"}), 404

    post = Post(
        title=title,
        content=content,
        user_id=user.id,
        category_id=category.id
    )

    session.add(post)
    session.commit()
    session.refresh(post)
    session.close()

    return jsonify({
        "message": "Post created successfully",
        "post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "category_id": post.category_id,
            "created_at": post.created_at.isoformat()
        }
    }), 201


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
