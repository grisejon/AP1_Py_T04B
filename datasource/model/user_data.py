from datasource.db import db
from sqlalchemy import Column, UUID as SQLAlchemyUUID, String


class UserData(db.Model):
    __tablename__ = 'users'

    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
