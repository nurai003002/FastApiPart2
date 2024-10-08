from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone: str
    birthday: date
    age: int
    # password: str
    # confirm_password: str
    # created_at: str

    