import sqlite3
from fastapi import FastAPI
app = FastAPI()
conn = sqlite3.connect("test.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

conn.commit()

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI SQLite example!"}