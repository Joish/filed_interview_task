import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from app import app
from base64 import b64encode
import unittest
from utils.api_client import ApiClient


class ProcessPayment(unittest.TestCase):
    def setUp(self):
        self.app = ApiClient(app)
        self.url_path = '/ProcessPayment'
        # self.app = app.test_client()

    def test_month_year_valid(self):
        data = {
            "CreditCardNumber": "4444333322221111",
            "CardHolder": "Joish",
            "ExpirationDate": "08/2023",
            "SecurityCode": "123",
            "Amount": 100
        }
        response = self.app.post(self.url_path,data)
        self.assertEqual(response.status_code, 200)

    def test_month_year_not_valid(self):
        data = {
            "CreditCardNumber": "4444333322221111",
            "CardHolder": "Joish",
            "ExpirationDate": "08-2023",
            "SecurityCode": "123",
            "Amount": 100
        }
        response = self.app.post(self.url_path,data)
        self.assertEqual(response.status_code, 400)
    
    def test_mandatory_fields_1(self):
        data = {
            "CreditCardNumber": "4444333322221111",
            "CardHolder": "",
            "ExpirationDate": "08/2023",
            "SecurityCode": "123",
            "Amount": 100
        }
        response = self.app.post(self.url_path,data)
        self.assertEqual(response.status_code, 400)
    
    def test_mandatory_fields_2(self):
        data = {
            "CreditCardNumber": "",
            "CardHolder": "ji",
            "ExpirationDate": "08/2023",
            "SecurityCode": "123",
            "Amount": 100
        }
        response = self.app.post(self.url_path,data)
        self.assertEqual(response.status_code, 400)

    def test_valid_cc_number(self):
        data = {
            "CreditCardNumber": "444433332222111",
            "CardHolder": "Joish",
            "ExpirationDate": "08/2023",
            "SecurityCode": "123",
            "Amount": 100
        }
        response = self.app.post(self.url_path,data)
        self.assertEqual(response.status_code, 400)
    
    def test_valid_cc_cvc(self):
        data = {
            "CreditCardNumber": "4444333322221111",
            "CardHolder": "Joish",
            "ExpirationDate": "08/2023",
            "SecurityCode": "12",
            "Amount": 100
        }
        response = self.app.post(self.url_path,data)
        self.assertEqual(response.status_code, 400)

    def test_valid_amount(self):
        data = {
            "CreditCardNumber": "4444333322221111",
            "CardHolder": "Joish",
            "ExpirationDate": "08/2023",
            "SecurityCode": "123",
            "Amount": -100
        }
        response = self.app.post(self.url_path,data)
        self.assertEqual(response.status_code, 400)
    
    def test_valid_amount_2(self):
        data = {
            "CreditCardNumber": "4444333322221111",
            "CardHolder": "Joish",
            "ExpirationDate": "08/2023",
            "SecurityCode": "123",
            "Amount": "-100"
        }
        response = self.app.post(self.url_path,data)
        self.assertEqual(response.status_code, 400)
        

if __name__ == '__main__':
    unittest.main()