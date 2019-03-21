import unittest
import requests
from flask import json
from app import app
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from unittest.mock import patch, Mock

def equal(a, b):
    #we will compare that request(a, which has bytes type) is equal to sample(b, which has dict type)
    a_dict = json.loads(a)
    if (a_dict == b):
        return True
    else:
        return False


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.browser = webdriver.Chrome(executable_path='/home/svetlana/back/chromedriver')

    def test_form(self):
        self.browser.get('http://127.0.0.1:5000/form/')
        time.sleep(0.5)
        elem_first_name = self.browser.find_element_by_name("first_name")
        elem_last_name = self.browser.find_element_by_name("last_name")
        elem_button = self.browser.find_element_by_id("button")
        elem_first_name.send_keys("Jack")
        time.sleep(1)
        elem_last_name.send_keys("Daniels")
        time.sleep(1)
        elem_button.send_keys(Keys.RETURN)
        time.sleep(1)
        self.assertIn('{\n  "first_name": "Jack", \n  "last_name": "Daniels"\n}', self.browser.page_source)
        self.browser.quit()

    def test_search_user(self):
        rv = self.app.get('/search_user/rick')
        data = {"name":"Rick Sanchez","nick":"rick","user_id":1}
        self.assertEqual(equal(rv.data, data), True)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)


    def test_search_chats(self):
        rv = self.app.get('/search_chat/rick&morty')
        data = {"chat_id":12,"is_group_chat":False,"last_message":"-","topic":"rick&morty"}
        self.assertEqual(equal(rv.data, data), True)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("application/json", rv.mimetype)


class JSONRPCTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


    @patch('app.send_message')
    def test_send_message(self, MockClass):
        my_mock = MockClass()

        my_mock.send_message.return_value = [
            {
                "id":1,
                "jsonrpc":"2.0",
                "result":"null"
            }
        ]

        response = my_mock.send_message(12,1,"test_message")
        self.assertEqual(response[0], json.loads('{"id":1,"jsonrpc":"2.0","result":"null"}'))
        self.assertEqual(MockClass.called, 1)


    #old_test
    '''
    def test_send_message(self):
        rv = self.app.post('/api/', data='{"jsonrpc":"2.0","method":"send_message","params":[12,1,"test_message"],"id":1}')
        sample = json.loads('{"id":1,"jsonrpc":"2.0","result":null}')
        self.assertEqual(json.loads(rv.data), sample)
    '''
    def test_read_message(self):
        rv = self.app.post('/api/', data='{"jsonrpc":"2.0","method":"read_message","params":[1,12,1205],"id":2}')
        sample = json.loads('{"id":2,"jsonrpc": "2.0","result": null}')
        self.assertEqual(json.loads(rv.data), sample)

 
    def test_get_chat_messages(self):
        rv = self.app.post('/api/', data='{"jsonrpc":"2.0","method":"get_chat_messages","params":[12,1],"id":3}')
        sample = json.loads('{"id":3,"jsonrpc": "2.0","result": {"0": [1201,12,1,"some_message_between0and1with_id=1"]}}')
        self.assertEqual(json.loads(rv.data), sample)



if __name__ == "__main__":
    unittest.main()
