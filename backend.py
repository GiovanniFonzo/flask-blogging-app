from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

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



@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
