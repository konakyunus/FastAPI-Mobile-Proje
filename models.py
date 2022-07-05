import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import config as _database
from pydantic import BaseModel



class User(_database.Base):
    __tablename__ = "accounts_user"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String)
    password = _sql.Column(_sql.String)

