from fastapi import FastAPI,Depends,Header,HTTPException
app = FastAPI()

def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token
@app.get("/secure-data")
def read_secure_data(x_token: str = Depends(verify_token)):
    return {"message": "Secure data retrieved successfully.", "x_token": x_token,"user": "johndoe"}

def get_current_user():
    return {"username": "johndoe"}

@app.get("/profile")
def read_profile(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

@app.get("/dashboard")
def read_dashboard(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}
