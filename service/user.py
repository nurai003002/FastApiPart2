from fastapi import HTTPException
from models.user import User
from sqlalchemy.orm import Session
from dto import user
import re

def create_user(data: user.User, db):
    user = User(username=data.username, first_name=data.first_name, last_name=data.last_name, phone=data.phone, birthday=data.birthday, age=data.age)
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username уже занят")
        
    phone_pattern = r'^\+996 \d{3} \d{2} \d{2} \d{2}$'
    if not re.match(phone_pattern, data.phone):
        raise HTTPException(status_code=500, detail='Номер телефона должен быть в формате +996 999 99 99 99')
    
    phone_validator = db.query(User).filter(User.phone == data.phone).first()
    if phone_validator:
        raise ValueError('Номер телефона уже используется')
    try:    
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)

    return user
    
def get_user(db:Session, id: int):
    user = db.query(User).filter(User.id==id).first()
    return user

def update(data: user.User, db: Session, id: int):
    user = db.query(User).filter(User.id==id).first()
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username уже занят")
    user.username = data.username
    first_name=data.first_name
    last_name=data.last_name
    phone=data.phone
    birthday=data.birthday
    age=data.age
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def delete(db:Session, id: int):
    user = db.query(User).filter(User.id==id).delete()
    db.commit()
    return user
