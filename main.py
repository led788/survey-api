from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKeyHeader, APIKey, APIKeyQuery, APIKeyCookie
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, RedirectResponse

import crud
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

API_KEY = "KJ38egx3eu832*G-s8733kjcV3A"
API_KEY_NAME = "apitoken"
COOKIE_DOMAIN = "survey-api.pydev.fun"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
# app = FastAPI()


@app.on_event("startup")
async def startup():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_api_key(api_key_query: str = Security(api_key_query),
                      api_key_header: str = Security(api_key_header),
                      api_key_cookie: str = Security(api_key_cookie)):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=403, detail="could not validate credentials"
        )


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        get_openapi(title="FastAPI security test", version=1, routes=app.routes)
    )
    return response


@app.get("/documentation", tags=["documentation"])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_KEY_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response


@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response


@app.get("/v1/surveys")
async def get_surveys(db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    """
    All Surveys list
    """
    return crud.get_surveys(db)


@app.get("/v1/survey/{survey_id}")
async def get_survey(survey_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    """
    Survey with questions list
    """
    return crud.get_survey(db, survey_id)


@app.put("/v1/survey/{survey_id}")
async def update_survey(survey_id: int, survey: schemas.SurveyCreate, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    """
    Survey update by id
    """
    return crud.update_survey(db=db, survey_id=survey_id, modified_survey=survey)


@app.delete("/v1/survey/{survey_id}")
async def delete_survey(survey_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    """
    Delete Survey by id
    """
    return crud.delete_survey(db=db, survey_id=survey_id)


@app.post("/v1/question/")
async def add_question(question: schemas.QuestionCreate, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    """
    Add new question
    """
    db_question = crud.add_question(db, question)
    return db_question


@app.put("/v1/question/{question_id}")
async def update_question(question_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    """
    Question update by id
    """
    return crud.update_question(db=db, question_id=question_id, modified_question=question)


@app.delete("/v1/question/{question_id}")
async def delete_question(question_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    """
    Delete Question by id
    """
    return crud.delete_question(db=db, question_id=question_id)


@app.get("/v1/answers/{survey_id}")
async def get_answers(survey_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    """
    Answers list by survey
    """
    return crud.get_answers(db, survey_id)


@app.post("/v1/answer/")
async def add_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    """
    Add new answer for survey
    """
    db_question = crud.add_answer(db, answer)
    return db_question


