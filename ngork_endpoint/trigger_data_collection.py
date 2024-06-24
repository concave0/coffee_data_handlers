import requests 

# Trigger data to turn on for the website start collecting both the ids then the and data 
class TriggerDataCollection: 
    def triggering(self, token:str, endpoint:str):
        headers = {
                    "Authorization": f"Bearer {token}"
                } 
        response = requests.get(url=endpoint,headers=headers)
        return response
    
