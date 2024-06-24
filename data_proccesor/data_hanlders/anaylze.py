from data_hanlders.data import Data
import json 

# Analysing the incoming data from data collector 
class AnalysingData: 
    # Analysis the incoming data 
    def analysing_data(self): 
        clean_coffee_data = {}
        data = Data()
        response_path = data.get_data()
        with open(response_path, "r") as file: 
            data = json.loads(json.dumps(json.load(file)))
            file.close()
        for coffee , facts in data.items():
            clean_coffee_data [coffee] = facts
        return clean_coffee_data
                         


