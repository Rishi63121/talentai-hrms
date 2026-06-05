#!/usr/bin/env python3
"""
Seed script: creates a default admin user so you can log in immediately.
Run once: python seed.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database.db import Base, engine, SessionLocal
from backend.models.models import User
from backend.services.auth_service import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()
if not db.query(User).filter(User.email == "admin@talentai.com").first():
    admin = User(
        name="Admin",
        email="admin@talentai.com",
        password_hash=hash_password("admin123"),
        role="admin",
    )
    db.add(admin)
    db.commit()
    print("✅ Admin user created — email: admin@talentai.com | password: admin123")
else:
    print("ℹ️  Admin user already exists.")
db.close()
