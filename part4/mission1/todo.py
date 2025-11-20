from typing import Any, Dict, List

import csv
import json
import os
import threading

from fastapi import APIRouter, FastAPI, HTTPException


# 전역 리스트 객체
todo_list: List[Dict[str, Any]] = []

_csv_lock = threading.Lock()
_csv_path = os.path.join(os.path.dirname(__file__), 'todo_list.csv')


def _load_from_csv() -> None:
    if not os.path.exists(_csv_path):
        return
    with _csv_lock:
        with open(_csv_path, 'r', encoding='utf-8', newline='') as fp:
            reader = csv.DictReader(fp)
            items: List[Dict[str, Any]] = []
            for row in reader:
                try:
                    item = json.loads(row.get('item', '{}'))
                    if isinstance(item, dict):
                        items.append(item)
                except json.JSONDecodeError:
                    continue
            todo_list.clear()
            todo_list.extend(items)


def _append_to_csv(item: Dict[str, Any]) -> None:
    file_exists = os.path.exists(_csv_path)
    with _csv_lock:
        with open(_csv_path, 'a', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(fp, fieldnames=['item'])
            if not file_exists:
                writer.writeheader()
            writer.writerow({'item': json.dumps(item, ensure_ascii=False)})


app = FastAPI(title='Todo API', version='0.1.0')

router = APIRouter(prefix='/todos', tags=['todos'])


@app.on_event('startup')
def on_startup() -> None:
    _load_from_csv()


@router.post('/add')
def add_todo(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict) or len(payload) == 0:
        raise HTTPException(status_code=400, detail='요청 본문이 비어 있습니다.')
    todo_list.append(payload)
    try:
        _append_to_csv(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail='CSV 저장 중 오류가 발생했습니다.') from exc
    return {'status': 'ok', 'item': payload, 'count': len(todo_list)}


@router.get('/list')
def retrieve_todo() -> Dict[str, Any]:
    return {'todo_list': todo_list, 'count': len(todo_list)}


app.include_router(router)

from __future__ import annotations

import csv
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, Body, FastAPI, HTTPException


CSV_FILE = Path(__file__).with_name('todos.csv')

# 메모리 상의 TODO 리스트
todo_list: List[Dict[str, Any]] = []

# 라우터
router = APIRouter(tags=['todos'])


def ensure_csv_file_exists() -> None:
    if not CSV_FILE.exists():
        with CSV_FILE.open('w', newline='', encoding='utf-8') as fp:
            writer = csv.DictWriter(fp, fieldnames=['id', 'data_json', 'created_at'])
            writer.writeheader()


def load_todos_from_csv() -> List[Dict[str, Any]]:
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
            # 서버가 부여한 메타 정보와 사용자 payload 병합
            todo.update(data)
            todo['id'] = row.get('id')
            todo['created_at'] = row.get('created_at')
            loaded.append(todo)
    return loaded


def append_todo_to_csv(todo: Dict[str, Any]) -> None:
    # CSV에는 서버 메타(id, created_at)와 사용자 payload를 JSON으로 저장
    record = {
        'id': str(todo.get('id') or ''),
        'data_json': json.dumps({k: v for k, v in todo.items() if k not in {'id', 'created_at'}}, ensure_ascii=False),
        'created_at': str(todo.get('created_at') or ''),
    }
    with CSV_FILE.open('a', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=['id', 'data_json', 'created_at'])
        writer.writerow(record)


def normalize_todo_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    normalized.update(payload)
    # 서버 생성 필드
    normalized['id'] = normalized.get('id') or str(uuid.uuid4())
    normalized['created_at'] = datetime.utcnow().isoformat() + 'Z'
    return normalized


@router.post('/todos', summary='새로운 TODO 추가')
def add_todo(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    # 보너스 과제: 빈 Dict 입력 시 경고 반환
    if not isinstance(payload, dict) or not payload:
        raise HTTPException(status_code=400, detail='빈 입력입니다. 하나 이상의 항목을 포함해 주세요.')

    todo = normalize_todo_payload(payload)
    todo_list.append(todo)
    append_todo_to_csv(todo)
    return {'todo': todo}


@router.get('/todos', summary='TODO 리스트 조회')
def retrieve_todo() -> Dict[str, Any]:
    return {'todos': todo_list}


app = FastAPI(title='TODO API', version='1.0.0')


@app.on_event('startup')
def on_startup() -> None:
    ensure_csv_file_exists()
    loaded = load_todos_from_csv()
    todo_list.clear()
    todo_list.extend(loaded)


app.include_router(router)



