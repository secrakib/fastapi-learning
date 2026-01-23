from pydantic import BaseModel

class Residence(BaseModel):
    city: str
    zip: int
    road: str

class Patient(BaseModel):
    name: str = 'abc'
    contact: str
    address: Residence


def info(info:Patient):
    print(info.name)
    print(info.contact)
    print(info.address)

    return None
    



information =info(
    Patient(
    name='ul',
    contact= '0123',
    address=Residence(
    city='ctg',
    zip=982,
    road='ti'

    ))
)

patient = Patient(
    #name='ul',
    contact= '0123',
    address=Residence(
    city='ctg',
    zip=982,
    road='ti'

    ))

temp = patient.model_dump(exclude={
    'name':True,
    'address':{
        'zip':True

    }

})
temp = patient.model_dump(exclude_unset=True)
print(temp,type(temp))
