from collections import deque 
import json 
import pywikibot
import mwparserfromhell

# Searching Wikipedia for Coffee Data
class SearchWiki(): 
 
    def __init__(self) -> None:
        self.search_query_queue  = deque()

    # Rate limting yourself to make sure and respect Wikimedia's Free API 
    def rate_limiter_yourself(self): 
       import time 
       print("Waiting a bit before the next call.")
       time.sleep(10)

    # Batch job to get Wikimedia data and then save to JSON
    def batch_get_articles(self, article_title:str):     
        filename="data_collector/raw_data/raw_data.json"
        with open(filename, "r") as file: 
            coffee_data = json.loads(json.dumps(json.load(file)))
            file.close()
 
        try: 
            if article_title not in coffee_data: # only get coffee if information has not been recorded 
                print(f"searcing for {article_title}")
                site = pywikibot.Site('en', 'wikipedia')
                page = pywikibot.Page(site, article_title)
                
                if page.exists():
                    text =  str(mwparserfromhell.parse(page.text))
                    data = { article_title : text }
                    self.save_to_json(data = data , filename = filename)
                else:
                    print("page does not exist.")
            else: 
                return  # do nothing 

        except Exception as e:
            error = f"failed to save and search for {article_title} because of {e}. \n"
            bugs = open("data_collector/bugs/bugs.txt","a")
            bugs.write(error)
            bugs.close()
            print(error) 
    
    # Save data to json 
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





