import json

class OrganizeData: 
    
    # Setting each data point and saving it
    def set_details(self, id: int , name: str , facts:str) -> int: 
        name = name 
        facts = facts 
        data = { name : id }
        # Saving the name and id. The name is the key and id is the value 
        self.save_to_json(data=data , filename="data_hanlders/ids_data/ids.json")
        self.save_to_json(data=data, filename="routes/ids_data/ids.json")
        return id 
    
    # Convert data to JSON and then save it
    def save_to_json(self, data, filename, indent=4):
        try:
            existing_data = {}
            with open(filename, 'r') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    pass
            existing_data.update(data)  

            with open(filename, 'w') as f:
                json.dump(existing_data, f, indent=indent)
                print(f"Data updated successfully in '{filename}'.")

        except IOError as e:
                print(f"Error updating data: {e}")
                


