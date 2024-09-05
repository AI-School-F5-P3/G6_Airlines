from sqlalchemy.orm import Session
import joblib

import model

with open('../model_pipeline.pkl', 'rb') as f:
    pipeline = joblib.load('../model_pipeline.pkl')

def post_data(db: Session, datax: model.FeatureSchema):

	x_dict = datax.model_dump()
	# new_data = model.Data(**datax.model_dump())
	# print(new_data)
	prediction = pipeline.predict([list(x_dict.values())])
	# if new_data:
	# 	return (new_data.prediction)
	# else:
	# 	return None

	return(prediction)

def get_all_data(db: Session):
	pass