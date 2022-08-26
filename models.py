from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from database import Base


class Answers(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, server_default=func.now())
    answers = Column(JSON)
    survey_id = Column(Integer, ForeignKey('surveys.id'))
    survey = relationship('Surveys')


class Surveys(Base):
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    start = Column(Integer)


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nextid = Column(Integer)
    yes = Column(Integer)
    no = Column(Integer)
    type = Column(String)
    question = Column(String)
    answers = Column(JSON)
    validation = Column(String)
    survey_id = Column(Integer, ForeignKey('surveys.id'))
    survey = relationship('Surveys', backref='questions')


