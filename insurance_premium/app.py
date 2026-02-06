from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import MODEL_VERSION,model,predict





app = FastAPI()




@app.get('/')
def home():
    return {'Home'}

@app.get('/health')
def health_check():
    return {
        'status':'OK',
        'MODEL_VERSION':MODEL_VERSION,
        'model_loaded':model is not None
    }

@app.post('/predict')
def predict_premium(data: UserInput):

    input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        prediction = predict(input)

        return JSONResponse(status_code=200, content={'predicted_category': prediction})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))




