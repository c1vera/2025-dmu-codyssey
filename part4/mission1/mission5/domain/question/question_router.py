from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import ContextManager

from database import get_db
from models import Question
from domain.question import question_schema

router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=list[question_schema.Question])
def question_list(db_context: ContextManager[Session] = Depends(get_db)):
    with db_context as db:
        _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
        return _question_list
