from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from service import user as UserService
from dto import user as UserDto

router = APIRouter()

@router.post("/", tags=["user"])
async def create(data: UserDto.User = None, db: Session = Depends(get_db)):
    return UserService.create_user(data, db)

@router.get('/{id}', tags=["user"])
async def get(id: int = None, db: Session = Depends(get_db)):
    return UserService.get_user(db, id)

@router.put("/{id}", tags=["user"])  
async def update(id: int = None, data:UserDto.User = None,  db: Session = Depends(get_db)):
    return UserService.update(data, db, id)

@router.delete("/{id}", tags=["user"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return UserService.delete(db, id)
