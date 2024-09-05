from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db import engine, SessionLocal
import model
import crud

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict/")
def predict(data: model.DataSchema, db:Session = Depends(get_db)):
    db_data = crud.post_data(db, data)
    if db_data:
        return f"predict: {db_data}"
    else:
        return {"Error"}