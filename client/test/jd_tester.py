import os
import unittest

from client import Client

SERVER_URL = os.getenv('SERVER_URL')


class Simple(unittest.TestCase):

    def setUp(self):
        # self.client = Client(SERVER_URL)

        self.data = [
            {'_key': 'first', 'data': '1'},
            {'_key': 'second', 'data': '2'},
            {'_key': 'third', 'data': '3'}
        ]

    def test_collections_connection(self):
        self.client.collection('test_collection')
        # collection_exits -> boolean
        self.assertTrue(self.client.collection_exists('test_collection'), "Fails connection to collection") # returns true if collection exits
        self.client.drop_collection('test_collection')
        self.assertFalse(self.client.collection_exists('test_collection'), "Fails collection still exits after drop")  # return true if collections drop correctly

    def test_data(self, data):
        for d in data:
            self.assertEqual(d['_key'], self.client.get(d['_key']))
            self.assertEqual(d['data'], self.client.get(d['data']))

    # Test for get, replace, update, create, delete operations
    def tester(self):

        self.test_collections_connection()

        # create, get
        self.client.collection('test_collection')
        for d in self.data:
            self.client.create(d)
        self.test_data(self.data)

        # update
        self.client.update('first', '3')
        new_data = [
            {'_key': 'third', 'data': '1'},
            {'_key': 'second', 'data': '2'},
            {'_key': 'first', 'data': '3'}
        ]
        self.test_data(new_data)

        # replace
        self.client.replace('second', '3')
        new_data = [
            {'_key': 'third', 'data': '1'},
            {'_key': 'second', 'data': '3'},
            {'_key': 'first', 'data': '3'}
        ]
        self.test_data(new_data)

        # delete
        self.client.delete('first')
        new_data = [
            {'_key': 'third', 'data': '1'},
            {'_key': 'second', 'data': '3'}
        ]
        self.test_data(new_data)

    def test_client(self, client: Client):
        self.client = client

        self.setUp()

        self.tester()