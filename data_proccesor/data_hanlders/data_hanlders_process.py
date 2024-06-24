from data_hanlders.anaylze import AnalysingData
from data_hanlders.data import Data 
from data_hanlders.id import generate_random_number 

# Handle the proccesing of incoming data from data collector and then sending it the database
class HandleProccesing:
    def store_data(self): 
        analyse = AnalysingData() 
        handling_data  = Data()
        data = analyse.analysing_data()
        for coffee , facts in data.items():
            id = generate_random_number(coffee_name=coffee)
            data = {coffee :[id, facts]}
            sending_data = handling_data.send_data(id=id, queue="database1", data=data, name=coffee , facts=facts) 
        return True 

