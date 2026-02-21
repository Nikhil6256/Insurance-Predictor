from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field, field_validator
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
import pandas as pd
from Schema.user_input import UserInput
from Model.predict import predict_output, Model, MODEL_VERSION


app = FastAPI()

@app.get('/')
def home():
    return {'message':'Insurance premium predictor'}

@app.get('/health')
def health():
    return {'statue':'OK',
            'Version':MODEL_VERSION,
            'model_loaded':Model is not None
            }

# pydantic model to validate incoming data

@app.post("/predict")

def predict_premium(data: UserInput):
    user_input = {
        "income_lpa": data.income_lpa,
        "occupation": data.occupation,
        "BMI": data.bmi,
        "Age_Group": data.age_group,  
        "Lifestyle Risk": data.lifestyle_risk,
        "City Tier": data.city_tier
    }

    # input_df = input_df[model.feature_names_in_]

    try:

        prediction = predict_output(user_input)

        return JSONResponse(status_code=200, content=prediction)
    except Exception as e:
        return JSONResponse(status_code=500,content={"error":str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("demo:app", host="0.0.0.0", port=8000)