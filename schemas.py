from pydantic import BaseModel


# Pydantic models

class QuestionCreate(BaseModel):
    survey_id: int
    nextid: int
    yes: int
    no: int
    type: str
    question: str
    answers: list[dict]
    validation: str

    class Config:
        orm_mode = True


class SurveyCreate(BaseModel):
    title: str
    start: int

    class Config:
        orm_mode = True


class AnswerCreate(BaseModel):
    answers: list[dict]
    survey_id: int

    class Config:
        orm_mode = True
