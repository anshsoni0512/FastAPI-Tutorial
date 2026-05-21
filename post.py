from pydantic import BaseModel, Field, computed_field
from typing import Literal, Optional
from fastapi import FastAPI, HTTPException
import json
from fastapi.responses import JSONResponse


app = FastAPI()

def load():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)
        


class Patient(BaseModel):
    id_no: str
    name:str
    age:int = Field(gt =0, lt = 120)
    city:str = Field(max_length=20)
    gender:Literal['male','female','others'] 
    height:float
    weight:float

    @computed_field
    @property
    def bmi(self)->float:
        bmi = self.weight/self.height**2
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi>25:
            return "Obese"
        else:
            return "Normal"

class UpdatePatient(BaseModel):
    name:Optional[str]
    age:Optional[int] = Field(gt =0, lt = 120)
    city:Optional[str] = Field(max_length=20)
    gender:Optional[Literal['male','female','others']] 
    height:Optional[float]
    weight:Optional[float]


@app.get('/')
def home():
    return {'message':'hello this is Home Page'}


@app.post('/create')
def create(patient:Patient):   # user data is sent by http request then Pydantic peforms all its validations and validotr functions then finally the cleaned data comes here.
    data = load()
    if patient.id_no in data:
        raise HTTPException(status_code = 400)
    data[patient.id_no] = patient.model_dump(exclude = 'id_no')   #getting dictonary in the patient.id key..

    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put('/edit/{id}')
def edit(id:str, patient_info:UpdatePatient):  # patient_info is a pydantic object..
    data = load()
    if id not in data:   
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        existing_patient_info = data[id]

        updated_patient_info = patient_info.model_dump(exclude_unset = True)

        for key,value in updated_patient_info.items():
            existing_patient_info[key] = value

        #existing has no id so include id because Patient class will not work without id..
        existing_patient_info['id_no'] = id
        newObject = Patient(**existing_patient_info)

        final_updated_info = newObject.model_dump(exclude = ['id_no'])
        data[id] = final_updated_info   # dont include id here..

        save_data(data)

        return JSONResponse(status_code=200, content ={'message': 'Patient info updated succesfully'})
    
@app.delete('/delete/{id}')
def delete(id):
    
    data = load()

    if id not in data:
        raise HTTPException(status_code=404, detail = 'Not found')   # the code stops here and gets out of funciton..
    
    del data[id]    # remove the the key and value from dictonary..
    save_data(data)
    return JSONResponse(status_code = 200, content = {'message':'Patient Deleted successfully'})



    




