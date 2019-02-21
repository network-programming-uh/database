import os
import unittest

from client import Client

SERVER_URL = os.getenv('SERVER_URL')

class Simple(unittest.TestCase):

    def setUp(self):
        self.client = Client(SERVER_URL)

        self.data = [
            {'_key': 'first', 'data': '1'},
            {'_key': 'second', 'data': '2'}
        ]

    def test_normal(self):
        self.client.collection('test')

        for d in self.data:
            self.client.create(d)
        
        for d in self.data:
            self.assertEqual(d, self.client.get(d['_key']))

        self.client.drop_collection('test')
