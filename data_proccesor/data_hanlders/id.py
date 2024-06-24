import random 
import json 

# Empty object to be hashed and created into an ID
class EmptyData: 
    pass 

# Create a random id to be stored and associated to the each coffee name.
def generate_random_number(coffee_name:str):
        with open("data_hanlders/ids_data/ids.json", "r") as file: 
            data = json.loads(json.dumps(json.load(file)))
            file.close()
        
        if coffee_name in data.keys():
             return data.get(coffee_name)
             
        elif coffee_name not in data.keys():
            start=0
            end=10
            number =  int(f"{random.randint(start, end - 1)}"  + f"{hash(EmptyData())}") 
            return number