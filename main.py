from datetime import timedelta
from fastapi.openapi.utils import get_openapi
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import django_pbkdf2_sha256
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
import schemas as _schemas
import services as _services

app = FastAPI()
_services.create_database()


@app.post("/token", response_model=_schemas.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user: _schemas.DataUser = _services.get_user_by_username(db=db, username=form_data.username)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = db_user.password
    if not django_pbkdf2_sha256.verify(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=_services.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _services.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    _services.upload_token(db=db, username=form_data.username, access_token=access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user/")
async def read_system_status(current_user: _schemas.User = Depends(_services.get_current_user)):
    return current_user



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Uzman Mobile Api",
        version="1.0.0",
        routes=app.routes,

    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema





app.openapi = custom_openapi