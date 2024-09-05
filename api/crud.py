from sqlalchemy.orm import Session

import model

def post_data(db: Session, data: model.DataSchema):
	new_data = model.Data(**data.model_dump())
	if new_data:
		return (new_data.prediction)
	else:
		return None

def get_all_data(db: Session):
	pass