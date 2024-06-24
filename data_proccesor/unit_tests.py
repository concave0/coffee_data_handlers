import unittest
import pika
from mq_queue.sender_queue_mq import SenderClientRabbitMq
from data_hanlders.data_hanlders_process import HandleProccesing , Data
from data_hanlders.anaylze import AnalysingData 


# Data proccessor application unit tests  
class AppilcationUnitTests(unittest.TestCase): 
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName) 

    # Testing sending and recieving with commication with the data proccesor
    def test_send_data(self): 
        data = "test"
        sending = SenderClientRabbitMq()
        sent = sending.send_data(target_queue_name="data_proccesor0", data=data)
        type_needed = pika.spec.Queue.DeclareOk.NAME
        self.assertTrue(sent.method.NAME==type_needed) 
    
    # Testing the update database
    def test_update_database(self): 
        handling_data = HandleProccesing()
        response = handling_data.store_data() 
        self.assertTrue(response==True) 

    # Testing getting data from data collector
    def test_get_data(self): 
        data =  Data()
        response = data.get_data()
        self.assertTrue(type(response)==str)
    
    # Testing fetch data using the coffee ID 
    def testing_data_fetch(self): 
        data =  Data()
        response = data.get_data_from_coffee_database('1274978100')
        self.assertTrue(type(response)==str)

    # Testing the data analysis
    def test_analysing_data(self): 
        analysis = AnalysingData()
        result = analysis.analysing_data()
        self.assertTrue(type(result)==dict)
    

if __name__ == '__main__':
    unittest.main()
