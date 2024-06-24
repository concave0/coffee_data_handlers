from  search.search_apis import  SearchWiki
from collections import deque

# Batch search and collect data 
class CollectDataFromSearch(): 

    # Using search apis garther data from wikipedia
    def __init__(self) -> None:
        self.wiki = SearchWiki()
        self.query_queue = deque()
        self.file_paths = dict()
    
    # Mapping the places in queue to Coffee items name and prompts for wikipedia 
    def settings(self): 
        coffee_map = {
            0 : "Coffee",
            1 : "Coffee preparation",
            2 : "List of coffee drinks", 
            3 : "Cappuccino", 
            4 : "Latte", 
            5 : "Frappuccino",
            6 : "Caffè mocha",
            7 : "Caffè americano", 
            8 : "Doppio",
            9 : "Caffè macchiato", 
            10 : "Cortado", 
            11 : "Ristretto",
            12 : "Lungo",
            13 : "Galão",
            14 : "Affogato",
            15 : "Espresso con panna",
            16 : "Cold brew coffee",
            17 : "Milk coffee",
            18 : "Drip coffee",
            19 : "Mazagran (drink)",
            20 : "moka pot", 
            21 : "French press", 
            22 : "percolator", 
            23 : "Coffee bean", 
            24 : "Espresso machine", 
            25 : "Coffee filter" , 
            26 : "Coffee percolator", 
            26 : "Espresso", 
            28 : "Coffee preparation", 
            29 : "Gaggia", 
            30 : "Coffeehouse", 
            31 : "List of coffeehouse chains", 
            32 : "Caffeine" , 
            33 : "Decaffeination" , 
            34 : "Coffee roasting", 
            35 : "Coffee preparation" , 
            36 : "Carafe", 
            37 : "Cold brew coffee", 
            38 : "Vacuum coffee maker", 
            39 : "Microfoam" , 
            40 : "Cuban espresso", 
            41 : "Caffè crema", 
            42 : "Liqueur coffee", 
            43 : "Asiático", 
            44 : "B-52 (cocktail)", 
            45 : "Black Russian", 
            46 : "Café com cheirinho" , 
            47 : "Caffè corretto" , 
            48 : "Carajillo" , 
            49 : "Cremat" , 
            50 : "Espresso martini" , 
            51 : "Karsk" , 
            52 : "Moretta (coffee)", 
            53 : "Piscoffee" , 
            54 : "Rüdesheimer Kaffee" , 
            55 : "White Russian (cocktail)", 
            56 : "Barraquito" , 
            57 : "Gunfire (drink)" , 
            58 : "Café de olla" , 
            59 : "Marocchino", 
            60 : "Caffè mocha", 
            61 : "Frappé coffee", 
            62 : "Mazagran (drink)", 
            63 : "Shakerato" , 
            64 : "Instant coffee", 
            65 : "Beaten coffee" , 
            66 : "Dalgona coffee" ,
            67 : "Café Touba", 
            68 : "Canned coffee", 
            69 : "Coffee milk", 
            70 : "Egg coffee", 
            71 : "Indian filter coffee", 
        
        }
        for number , coffee_prompt in coffee_map.items(): 
            self.query_queue.append(coffee_prompt)

    # Running batch job to collect data and rate limiting   
    def batch_job_collect(self): 
        while len(self.query_queue) > 0: 
            query = self.query_queue.popleft()
            self.wiki.batch_get_articles(query)
            self.wiki.rate_limiter_yourself()

    
