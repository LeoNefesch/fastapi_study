from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import ValidationException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI(
    title="Trading App"
)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )

fake_users = [
    {"id": 1, "role": "admin", "name": ["Bob"]},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
    {"id": 4, "role": "investor", "name": "Homer", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
]
fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


class Trades(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])  # валидация серверных данных
def get_user(user_id: int):
    print([user for user in fake_users if user.get("id") == user_id])
    return [user for user in fake_users if user.get("id") == user_id]


@app.post("/trades")
def add_trades(trades: List[Trades]):  # валидация клиентских данных
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}


if __name__ == "__main__":  # Rerun: Ctrl + F5
    uvicorn.run("main:app", host='127.0.0.1', port=8000, workers=3)
