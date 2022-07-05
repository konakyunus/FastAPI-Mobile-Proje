from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal




router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

