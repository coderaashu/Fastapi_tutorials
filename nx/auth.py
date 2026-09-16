from fastapi import FastAPI, Depends, HTTPException
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

app = FastAPI()

# JWT configuration
SECRET_KEY = "superb secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing configuration
# pbkdf2_sha256 avoids the bcrypt/passlib compatibility issue seen in this environment.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Dummy user database
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("pass")
    }
}


def normalize_password(password: str) -> str:
    if password is None:
        raise ValueError("Password is required")
    if not password:
        raise ValueError("Password cannot be empty")
    return password


def hash_password(password: str):
    return pwd_context.hash(normalize_password(password))


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(normalize_password(plain_password), hashed_password)

def create_token(data: dict):    #token creation function
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#login api(OAuth2 form)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_data = {"sub": user["username"]}
    token = create_token(token_data)
    return {"access_token": token, "token_type": "bearer"}

#token verify
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

#protected api endpoint
@app.get("/protected")
async def protected(username: str = Depends(verify_token)):
    return {"message": f"Hello, {username}!"}

"""
#login api(to generate token)
@app.post("/login")
async def login(username: str, password: str):
    # Replace this with your actual authentication logic
    if username == "admin" and password == "password":
        token_data = {"sub": username}
        token = create_token(token_data)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
"""
"""
#token verification function
def verify_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

#protected api endpoint
@app.get("/protected")
async def protected(username: str = Depends(verify_token)):
    return {"message": f"Hello, {username}!"}
"""