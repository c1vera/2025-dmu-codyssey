from __future__ import annotations

import csv
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, FastAPI, HTTPException, status

from model import TodoItem

CSV_FILE = Path(__file__).with_name('todos.csv')

# 메모리 상의 TODO 리스트
todo_list: List[Dict[str, Any]] = []

# 라우터
router = APIRouter(tags=['todos'])


def ensure_csv_file_exists() -> None:
    """CSV 파일이 없으면 헤더를 포함하여 생성합니다."""
    if not CSV_FILE.exists():
        with CSV_FILE.open('w', newline='', encoding='utf-8') as fp:
            writer = csv.DictWriter(fp, fieldnames=['id', 'data_json', 'created_at'])
            writer.writeheader()


def load_todos_from_csv() -> List[Dict[str, Any]]:
    """CSV 파일에서 모든 Todo를 읽어옵니다."""
    if not CSV_FILE.exists():
        return []

    loaded: List[Dict[str, Any]] = []
    with CSV_FILE.open('r', newline='', encoding='utf-8') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            try:
                data = json.loads(row.get('data_json') or '{}')
            except json.JSONDecodeError:
                data = {}
            
            todo: Dict[str, Any] = {}
            # 서버가 부여한 메타 정보와 사용자 데이터 병합
            todo.update(data)
            todo['id'] = row.get('id')
            todo['created_at'] = row.get('created_at')
            loaded.append(todo)
    return loaded


def save_all_todos_to_csv() -> None:
    """메모리에 있는 모든 Todo를 CSV 파일에 덮어씁니다 (수정/삭제 시 사용)."""
    with CSV_FILE.open('w', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=['id', 'data_json', 'created_at'])
        writer.writeheader()
        
        for todo in todo_list:
            # 저장할 때는 id와 created_at을 제외한 나머지 데이터를 data_json으로 묶음
            data_to_save = {k: v for k, v in todo.items() if k not in {'id', 'created_at'}}
            record = {
                'id': todo.get('id'),
                'data_json': json.dumps(data_to_save, ensure_ascii=False),
                'created_at': todo.get('created_at'),
            }
            writer.writerow(record)


def append_todo_to_csv(todo: Dict[str, Any]) -> None:
    """새로운 Todo 하나를 CSV 파일 끝에 추가합니다."""
    data_to_save = {k: v for k, v in todo.items() if k not in {'id', 'created_at'}}
    record = {
        'id': todo.get('id'),
        'data_json': json.dumps(data_to_save, ensure_ascii=False),
        'created_at': todo.get('created_at'),
    }
    with CSV_FILE.open('a', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=['id', 'data_json', 'created_at'])
        writer.writerow(record)


@router.post('/todos', summary='새로운 TODO 추가', status_code=status.HTTP_201_CREATED)
def add_todo(item: TodoItem) -> Dict[str, Any]:
    """새로운 Todo를 생성합니다."""
    todo_data = item.dict()
    
    # 서버 생성 필드 추가
    todo_data['id'] = str(uuid.uuid4())
    todo_data['created_at'] = datetime.utcnow().isoformat() + 'Z'
    
    todo_list.append(todo_data)
    append_todo_to_csv(todo_data)
    
    return todo_data


@router.get('/todos', summary='TODO 리스트 조회')
def retrieve_todos() -> Dict[str, Any]:
    """모든 Todo 리스트를 반환합니다."""
    return {'todos': todo_list}


@router.get('/todos/{todo_id}', summary='개별 TODO 조회')
def get_single_todo(todo_id: str) -> Dict[str, Any]:
    """ID를 통해 특정 Todo를 조회합니다."""
    for todo in todo_list:
        if todo['id'] == todo_id:
            return todo
    
    raise HTTPException(status_code=404, detail='Todo not found')


@router.put('/todos/{todo_id}', summary='TODO 수정')
def update_todo(todo_id: str, item: TodoItem) -> Dict[str, Any]:
    """ID를 통해 특정 Todo를 수정합니다."""
    for index, todo in enumerate(todo_list):
        if todo['id'] == todo_id:
            # 기존 메타 데이터(id, created_at)는 유지하고 내용만 업데이트
            updated_data = item.dict()
            updated_data['id'] = todo['id']
            updated_data['created_at'] = todo['created_at']
            
            todo_list[index] = updated_data
            save_all_todos_to_csv()
            return updated_data
            
    raise HTTPException(status_code=404, detail='Todo not found')


@router.delete('/todos/{todo_id}', summary='TODO 삭제')
def delete_single_todo(todo_id: str) -> Dict[str, Any]:
    """ID를 통해 특정 Todo를 삭제합니다."""
    for index, todo in enumerate(todo_list):
        if todo['id'] == todo_id:
            del todo_list[index]
            save_all_todos_to_csv()
            return {'message': 'Todo deleted successfully'}
            
    raise HTTPException(status_code=404, detail='Todo not found')


app = FastAPI(title='Fully Working Todo API', version='1.0.0')


@app.on_event('startup')
def on_startup() -> None:
    """앱 시작 시 CSV 파일 확인 및 데이터 로드."""
    ensure_csv_file_exists()
    loaded = load_todos_from_csv()
    todo_list.clear()
    todo_list.extend(loaded)


app.include_router(router)







