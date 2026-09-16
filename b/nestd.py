from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class User(BaseModel):
    name: str
    age: int
    email: str
    address: Address

@app.post("/users")
def create_user(user: User):
    return {"message": "User created successfully", "user": user}
