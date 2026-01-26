from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
from fastapi.responses import JSONResponse

app = FastAPI()

def load_data()->dict:
    '''
    Take patients json file from folder and 
    convert to dict
    
    :return: dict containing data of patients.json 
    :rtype: dict
    '''
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

def unload_data(data:dict)-> dict:
    with open('patients.json', 'w') as file:
            json.dump(data, file, indent=4)
    return None

@app.get('/')
def hello():
    return {'messege': 'Hello world'}

@app.get('/about')
def about():
    return load_data()

@app.get('/patient_info/{id}')
def patient_info(id:str = Path(...,description = 'Info of patient',examples = 'P001')):

    data = load_data()

    return {'patient_info': data[id]}

@app.put('/update_info/{id}',description='Choose between field --> name,city,age,gender,height,weight,bmi,verdict')
def update_info(id:str,field:str,new_info:int | str):

    data = load_data()
    
    if id not in data:
        raise HTTPException(status_code=404, detail='Item not found')
    else:
        data[id][field]=new_info
        unload_data(data)

        return {'updated patient_info': data[id]}

@app.delete('/delete_info/{id}')
def delete_info(id:str):

    data = load_data()

    if id not in data:
        raise HTTPException(status_code=404, detail='Item not found')
    
    else:
        deleted = id
        del data[id]

        unload_data(data)

        return {'removed patient_info id': deleted}



@app.post('/create_info/{id}')
def create_info(id:str,name:str,city:str,age:int,gender:str,height:float,weight:float,bmi:float,verdict:str):

    data = load_data()
    
    data[id] = {}
    data[id]["name"] = name
    data[id]["city"] = city
    data[id]["age"] = age
    data[id]["gender"] = gender
    data[id]["height"] = height
    data[id]["weight"] = weight
    data[id]["bmi"] = bmi
    data[id]["verdict"] = verdict

    unload_data(data)

    return {'Added patient_info': data[id]}

@app.get('/sort_info/{id}')
def sort_info(id: str = Path(...,description='Patient id'), sort_by: str = Query(...,description='Sort by bmi or height or weight'), order:str=Query('asc',description='asc or des')):
     
    sort_by_values = ['bmi','height','weight']

    data = load_data()
    if id in data:
        temp_data = data
    else:
        raise HTTPException(status_code=404,detail='id not found')

    order_type = ['asc','des']
    if order not in order_type:
        raise HTTPException(status_code=404, detail='invalid order type')
    else:
        order = True if order == 'asc' else False

    sort_by_values = ['bmi','height','weight']

    if sort_by in sort_by_values:
        sorted_data = sorted(temp_data.values(), key = lambda x: x.get(sort_by,0), reverse=order)
    else:
        raise HTTPException(status_code=404, detail='sort by value incorrect')
    
    return sorted_data



class Create_info_with_v(BaseModel):
    id : Annotated[str,Field(...,description='id of patient',examples=['P001'])]
    name: Annotated[str,Field(...,description='name of patient',examples=['Karim'])]
    city: Annotated[str,Field(...,description='city of patient',examples=['syl'])]
    age: Annotated[int,Field(...,description='age of patient',examples=[23])]
    gender:Annotated[Literal['Male','Female'],Field(...,description='id of patient',examples=['Male'])]
    height:Annotated[float,Field(...,description='height of patient',examples=[23.4])]
    weight: Annotated[float,Field(...,description='weight of patient',examples=[12.3])]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = self.weight / (self.height ** 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            verdict = "Underweight"
        elif self.bmi < 25:
            verdict = "Normal weight"
        elif self.bmi < 30:
            verdict = "Overweight"
        else:
            verdict = "Obese"

        return verdict


@app.post('/create_info_with_v')
def create_info(info: Create_info_with_v):


    data = load_data()

    if info.id in data:
        raise HTTPException(409,detail='Patient exists')
    
    data[info.id] = info.model_dump(exclude='id')

    unload_data(data)

    return JSONResponse(status_code=201, content= {'Patient_id':info.id, 'Data':data[info.id]})