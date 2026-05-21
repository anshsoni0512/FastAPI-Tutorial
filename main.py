from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field

app = FastAPI() # create an object of fastapi


class Patient(BaseModel):
    name:str
    age:int = Field(gt =0, lt = 120)
    city:str = Field(max_length=20)
    gender:str
    height:float
    weight:float



# everytime we wnat patients data so creating a fuction so that we can get data
def load():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

@app.get("/")  # if you want to fetch soemthign from server you use get..
def hello():
    return {'message':'hello'}
# this is our first api endpoint ..

@app.get("/about")
def about():
    return {'message':"this is the about page"}
# this is the second api endpoint

# A full API is usually a collection of multiple such endpoints.
# GET = fetching data from the server and POST = sending data to the server

@app.get("/view")
def view():
    data = load()
    return data

@app.get('/view/{id}')    #Path Parameters..
def viewid(id = Path(...,description="Id of the patient", example="P001")): 
    data = load()   # so here data is dictonary
    if id in data:
        return data[id]
    raise HTTPException(status_code = 404, detail="Patient not found")

@app.get('/sort')  # here you dont have to provide any parameter.
def sort(sort_by = Query(..., description="Sort on the basis of height, weight and BMI"), order = Query("asc", description="sort in asc or desc order")):
    valid_filter = ["height", "weight", "bmi"]
    if sort_by not in valid_filter:
        raise HTTPException(status_code=400)
    if order not in ['asc','dsc']:
        raise HTTPException(status_code=400)

    data = load()
    
    if order=='asc':
        sort_order = False
    else:
        sort_order = True

    
    sorting = sorted(data.values(),key = lambda x:x.get(sort_by,0),reverse = sort_order)
    return sorting


# # Without Path() and Query()
# @app.get('/view/{id}')
# def viewid(id: str):          # FastAPI auto-detects it as a path parameter
#     ...

# @app.get('/sort')
# def sort(sort_by: str, order: str = "asc"):   # FastAPI auto-detects as query params
#     ...


