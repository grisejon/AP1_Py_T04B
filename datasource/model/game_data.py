from uuid import UUID
from datasource.db import db
from sqlalchemy import Column, UUID as SQLAlchemyUUID, JSON, String


class GameData(db.Model):
    __tablename__ = 'games'

    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True)
    board_matrix = Column(JSON, nullable=False)
    state = Column(String, nullable=False)
    player_one_id = Column(SQLAlchemyUUID(as_uuid=True), nullable=True)
    player_two_id = Column(SQLAlchemyUUID(as_uuid=True), nullable=True)
    player_one_symbol = Column(String, nullable=True)
    player_two_symbol = Column(String, nullable=True)
    current_turn_user_id = Column(SQLAlchemyUUID(as_uuid=True), nullable=True)
    against_computer = Column(db.Boolean, default=False)
