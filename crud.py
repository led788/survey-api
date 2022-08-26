from sqlalchemy.orm import Session
# from models import Surveys, Questions
import models
import schemas


def get_surveys(db: Session):
    return db.query(models.Surveys).all()


def get_survey(db: Session, survey_id: int):
    survey = db.query(models.Surveys).filter(models.Surveys.id == survey_id).first()
    _ = survey.questions
    return survey


def update_survey(db: Session, survey_id: int, modified_survey: schemas.SurveyCreate):
    survey = db.query(models.Surveys).filter(models.Surveys.id == survey_id).first()
    modified = dict(modified_survey)
    for key in dict(modified):
        setattr(survey, key, modified[key])
    db.commit()
    return survey_id


def delete_survey(db: Session, survey_id: int):
    survey = db.query(models.Surveys).filter(models.Surveys.id == survey_id).first()
    db.delete(survey)
    db.commit()
    return survey_id


def add_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Questions(survey_id=question.survey_id,
                                   nextid=question.nextid,
                                   yes=question.yes,
                                   no=question.no,
                                   type=question.type,
                                   question=question.question,
                                   answers=question.answers,
                                   validation=question.validation)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question.id


def update_question(db: Session, question_id: int, modified_question: schemas.QuestionCreate):
    question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    modified = dict(modified_question)
    for key in dict(modified):
        setattr(question, key, modified[key])
    db.commit()
    return question_id


def delete_question(db: Session, question_id: int):
    question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    db.delete(question)
    db.commit()
    return question_id


def get_answers(db: Session, survey_id: int):
    return db.query(models.Answers).filter(models.Answers.survey_id == survey_id).all()


def add_answer(db: Session, answer: schemas.AnswerCreate):
    db_answers = models.Answers(survey_id=answer.survey_id,
                                answers=answer.answers)
    db.add(db_answers)
    db.commit()
    db.refresh(db_answers)
    return db_answers.id
