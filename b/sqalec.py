from sqlalchemy import create_engine,Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base,Session
from fastapi import FastAPI, Depends

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"    #database URL for SQLite database
#engine created 
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
#sessions for db ops
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#base class for models
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)



Base.metadata.create_all(bind=engine)     #create the database tables

def get_db():       #
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/todos/")
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(title=title,description="False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"message": "Todo created successfully!", "todo": todo}
#read all todos
@app.get("/todos/")
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return {"total": len(todos), "todos": todos}

@app.get("/todos/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        return {"message": "Todo not found!"}
    return {"todo": todo}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, description: str, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        return {"message": "Todo not found!"}
    todo.description = description
    db.commit()
    db.refresh(todo)
    return {"message": "Todo updated successfully!", "todo": todo}
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        return {"message": "Todo not found!"}
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully!"}
    
# @app.get("/")
# def home(db: Session = Depends(get_db)):
    
#     return {"message": "db connected successfully!"}

