from fastapi import HTTPException
from models.user import User
from sqlalchemy.orm import Session
from dto import user
import re

def create_user(data: user.User, db):
    user = User(username=data.username, first_name=data.first_name, 
                last_name=data.last_name, phone=data.phone, birthday=data.birthday,
                age=data.age, password=data.password, confirm_password=data.confirm_password,
                created_at=data.created_at)
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username уже занят")
        
    phone_pattern = r'^\+996 \d{3} \d{2} \d{2} \d{2}$'
    if not re.match(phone_pattern, data.phone):
        raise HTTPException(status_code=500, detail='Номер телефона должен быть в формате +996 XXX XX XX XX')
    
    phone_validator = db.query(User).filter(User.phone == data.phone).first()
    
    if len(data.password) < 8:
        raise HTTPException(status_code=500, detail='Пароль должен быть не менее 8 символов')
    
    for i in range(len(data.password) - 2):
        if data.password[i] == data.password[i + 1] == data.password[i + 2]:
            raise HTTPException(status_code=500, detail='Пароль не должен содержать три одинаковых символа подряд')

    if not any(char.isdigit() for char in data.password):
        raise HTTPException(status_code=500, detail='Пароль должен содержать хотя бы одну цифру')
    
    if not any(char.isalpha() for char in data.password):
        raise HTTPException(status_code=500, detail='Пароль должен содержать хотя бы одну букву')

    if data.password != data.confirm_password:
        raise HTTPException(status_code=500, detail='Пароли разные')
    
    if phone_validator:
        raise HTTPException(status_code=500, detail='Номер телефона уже используется')

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
    phone_pattern = r'^\+996 \d{3} \d{2} \d{2} \d{2}$'
    if not re.match(phone_pattern, data.phone):
        raise HTTPException(status_code=500, detail='Номер телефона должен быть в формате +996 XXX XX XX XX')
    if data.age <= 0:
        raise HTTPException(status_code=500, detail='Возраст не должен быть меньше 0')
    
    phone_validator = db.query(User).filter(User.phone == data.phone).first()
    
    if len(data.password) < 8:
        raise HTTPException(status_code=500, detail='Пароль должен быть не менее 8 символов')
    
    for i in range(len(data.password) - 2):
        if data.password[i] == data.password[i + 1] == data.password[i + 2]:
            raise HTTPException(status_code=500, detail='Пароль не должен содержать три одинаковых символа подряд')

    if not any(char.isdigit() for char in data.password):
        raise HTTPException(status_code=500, detail='Пароль должен содержать хотя бы одну цифру')
    
    if not any(char.isalpha() for char in data.password):
        raise HTTPException(status_code=500, detail='Пароль должен содержать хотя бы одну букву')

    if data.password != data.confirm_password:
        raise HTTPException(status_code=500, detail='Пароли разные')
    
    if phone_validator:
        raise HTTPException(status_code=500, detail='Номер телефона уже используется')
    
    
    user.username = data.username
    first_name=data.first_name
    last_name=data.last_name
    phone=data.phone
    birthday=data.birthday
    password=data.password
    confirm_password=data.confirm_password
    age=data.age
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def delete(db:Session, id: int):
    user = db.query(User).filter(User.id==id).delete()
    db.commit()
    return user
