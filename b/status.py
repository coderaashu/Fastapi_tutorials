from fastapi import FastAPI,status,HTTPException,Request
from fastapi.responses import JSONResponse
app = FastAPI()

class UserNotFoundException(Exception):
    def __init__(self,name:str):
        self.name=name

@app.exception_handler(UserNotFoundException)
def user_not_found_exception_handler(request:Request,exc:UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status": "error",
            "message": f"User '{exc.name}' not found."
        }
    )
@app.get("/user/{name}")
def get_user_by_name(name:str):
    if name != "John Doe":
        raise UserNotFoundException(name=name)
    return {
        "status": "success",
        "message": "User retrieved successfully.",
        "data": {
            "name": name,
            "age": 30
        }
    }





#@app.post("/status", status_code=status.HTTP_201_CREATED)
#def create_status():
 #   return {"message": "Status created successfully."}


#@app.get("/user")
#def get_user():
 #   return{
  #      "status": "success",
   #     "message": "User retrieved successfully.",
    #    "data": {
     #       "name": "John Doe",
      #      "age": 30
       # }
    #}

"""
@app.get("/user/{user_id}")
def get_user_by_id(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return {
        "status": "success",
        "message": "User retrieved successfully.",
        "data": {
            "id": user_id,
            "name": "John Doe",
            "age": 30
        }
    }
"""