import sqlalchemy.orm as _orm
import fastapi as _fastapi
import services as _services, schemas as _schemas
from config import SessionLocal
from router import router
from datetime import datetime, timedelta
from typing import List, Union
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError


app = FastAPI()

app.include_router(router, prefix="/book", tags=["book"])

_services.create_database()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class User(BaseModel):
    id: int
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class DataUser(BaseModel):
    username: str
    password: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username2: str, username: str):
    if username == username2:
       return username
    return False


def authenticate_user(username2: str, password2: str, username: str, password: str):
            if username2 != username:
                return False
            if password2 != password:
                return False
            return True


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        db_user: DataUser = _services.get_user_by_username(db=db, username=username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db_user.username, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



""""" Kullanıcı Kaydı Oluşturma
@app.post("/users/", response_model=_schemas.User)
def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    return _services.create_user(db=db, user=user)

"""

@app.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: _orm.Session = _fastapi.Depends(_services.get_db)):
        db_user: DataUser = _services.get_user_by_username(db=db, username=form_data.username)
        user2 = authenticate_user(db_user.username, db_user.password, form_data.username, form_data.password)
        if user2 == True :
             access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
             access_token = create_access_token(
             data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


@app.get("/status/")
async def read_system_status(current_user: User = Depends(get_current_user)):
    return {"status": "ok"}


