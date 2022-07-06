import sqlalchemy as _sql

import config as _database


class User(_database.Base):
    __tablename__ = "accounts_user"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    password = _sql.Column(_sql.String)
    last_login = _sql.Column(_sql.DateTime)
    is_superuser = _sql.Column(_sql.Boolean)
    username = _sql.Column(_sql.String)
    first_name = _sql.Column(_sql.String)
    last_name = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String)
    is_staff = _sql.Column(_sql.Boolean)
    is_active = _sql.Column(_sql.Boolean)
    mobile_phone = _sql.Column(_sql.String)
    avatar = _sql.Column(_sql.String)
    is_deleted = _sql.Column(_sql.Boolean)
    date_joined = _sql.Column(_sql.Date)
    job_title = _sql.Column(_sql.String)
    token = _sql.Column(_sql.String)
