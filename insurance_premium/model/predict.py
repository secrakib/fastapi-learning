import pickle
import pandas as pd

# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION = 1.0

def predict(user_input:dict)->str:
    input_df = pd.DataFrame([user_input])
    prediction = model.predict(input_df)[0]

    return prediction

