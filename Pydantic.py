from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field

from typing import List, Dict, Optional

# this is our Pydantic class
class Patient(BaseModel):
    name: Optional[str] = Field(default = None, max_length=30, title="Name of the user", description="This column provides the description of the 'Name' column. These are the metadata both title and description.")

    email: Optional[EmailStr] = None

    linkedin_url: Optional[AnyUrl] = None

    age: int = Field( gt = 0, lt = 120, strict = True ) 

    bmi: Optional[float] = Field(default=None, gt = 0) 

    allergies:List[str] = Field(max_length=5)  # no one can add more than 5 allergies

    contact:Optional[Dict[str,str]] = None


    @field_validator('email')  # mention name of the field you have to do custom data vlaidaitons
    @classmethod   # you have to mention that this is a class method
    def email_validator(cls,value):   # value is the email complete address
        domain = value.split('@')
        if domain[-1] not in ['icici.com', 'hdfc.com']:
            raise ValueError("Domain not valid")
        return value
    


    # YOU CAN TRANSFORM YOUR DATA USING CUSTOM DATA VALIDATIONS..
    @field_validator('name')    
    @classmethod
    def transform_name(cls,value):
        return value.upper()
    
    # cls is like self..


    # IF YOU WANT TO MAKE VALIDATIONS THAT HAS MORE THNA 1 COULUMN THEN USE MODEL_VALIDATOR..
    @model_validator(mode = 'after')   # mode is compulsory to mention
    @classmethod
    def emergency_contact_above_60(cls,model):
        if model.age>60 and 'emergency' not in model.contact:
            raise ValueError("If age is greater than 60 then there should be one emergency contact.")
        return model



    @computed_field
    @property
    def calculate_bmi(self)->float:  # you cant divide None/100 = error
        if self.bmi is None:                        # ✅ handle None case
            return None
        bmi = (self.bmi/(self.age**2))
        return bmi


def insert1(patient:Patient):   # now this function is getting a pydantic object not the values..
    print(patient.name)
    print(type(patient.name))

    print(patient.age)
    print(type(patient.age))

    print("this is internal BMI field ",patient.calculate_bmi)   # this field is created after user input the data..

    print("inserted")

model = Patient(name = "ansh", age = 12, bmi = 10, allergies = [],contact = {})      #model = Patient({"name":"Ansh","age":22})
insert1(model)
# when you initializa the model you have to provide all data like alleriges, contact. If its not then give empty.

model1 = Patient(name = "Rytham",age = 22, bmi = "20", allergies = ['cough','cold'],contact = {"email":"abc@abc.com","phone":"123456789"})
insert1(model1)

model2 = Patient(name = "Akshar", age = 35, allergies = ['ish'])
insert1(model2)
# now we have written optional so there will be no error if you dont provide bmi and contact..

model3 = Patient(name = 'Laney', age = 40, allergies = ['puple hair'], email = 'anshsoni@icici.com')
insert1(model3)
# if the format of email is not correct then it will throw an error.

model4 = Patient(name = 'Nagi', age = 10, allergies = ['black hair'], email = 'anshsoni@hdfc.com',linkedin_url="https://www.linkedin.com")
insert1(model4)

model5 = Patient(name = 'BMI PATIENT', age = 10, bmi = 100, allergies = ['black hair'], email = 'anshsoni@icici.com',linkedin_url="https://www.linkedin.com")
insert1(model5)

t1 = model4.model_dump()  #Dict
print("This is t1",t1)

t2 = model5.model_dump_json(include = ['name', 'email'])  #JSON  which columns to include??
print("This is t2", t2)

