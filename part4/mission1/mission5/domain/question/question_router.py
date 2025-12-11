from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import ContextManager

from database import get_db
from models import Question
from domain.question import question_schema, question_crud

router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=list[question_schema.Question])
def question_list(db_context: ContextManager[Session] = Depends(get_db)):
    with db_context as db:
        _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
        return _question_list

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db_context: ContextManager[Session] = Depends(get_db)):
    with db_context as db:
        question_crud.create_question(db=db, question_create=_question_create)
