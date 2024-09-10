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
def predict(data: model.FeatureSchema, db: Session = Depends(get_db)):
    result = crud.post_data(db, data)
    if result:
        # Suponiendo que 'result' contiene una predicción de si el cliente estará satisfecho
        satisfaction_prediction = "satisfecho" if result else "insatisfecho"
        return {"msg": "ok", "satisfaction_prediction": satisfaction_prediction}
    else:
        return {"msg": "error"}