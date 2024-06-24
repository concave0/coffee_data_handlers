import requests 

# Giving the Ngork server token to the website server.
class TokenInTransit: 
    def give(self, token:str, endpoint:str):
        headers = {
                    "Authorization": f"Bearer {token}"
                } 
        response = requests.post(url=endpoint,headers=headers)
        return response