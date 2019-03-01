import os
import unittest
from multiprocessing import Process

from client import Client

SERVER_URL = os.getenv('SERVER_URL')


class Simple2(unittest.TestCase):
    def setUp(self):
        self.client = Client(SERVER_URL)

        self.workers_data = [
            {'_key': 1, 'Name': 'Juan', 'Last Name':'García','Age': '19','State':'Working'},
            {'_key': 2, 'Name': 'Carla','Last Name':'Díaz', 'Age': '28','State':'Working'},
            {'_key': 3, 'Name': 'Pepe', 'Last Name':'Navarro','Age': '25','State':'Resting'},
            {'_key': 4, 'Name': 'Roxana', 'Last Name':'Colmenero','Age': '20','State':'Resting'},
        ]

        self.cities_data = [
            {'_key': 1, 'Name': 'La Habana','Country':'Cuba'},
            {'_key': 2, 'Name': 'New York', 'Country': 'EEUU'},
            {'_key': 3, 'Name': 'Caracas', 'Country': 'Venezuela'},
            {'_key': 4, 'Name': 'Bogotá', 'Country': 'Colombia'},
            {'_key': 5, 'Name': 'Buenos Aires', 'Country': 'Argentina'},
        ]
        self.operators_fun = [
            self.client.create,self.client.update,self.client.replace,self._check_delete
        ]


        row_to_create = {'_key': 6, 'Name': 'Santiago de Chile', 'Country': 'Chile',
                         'Other_stuff': [1, 2, 3, 4, 5]
                         }
        row_to_update = {'_key': 2, 'Name': 'Ottawa', 'Country': 'Canada'}
        to_replace = {'_key': 3, 'Name': 'Ciudad de Mexico', 'Country':
            'Mexico', 'Other_field': True
                      }
        to_delete = row_to_create['_key']
        self.operational_objects = [
            row_to_create,(row_to_update['_key'],row_to_update),
            (to_replace['_key'],to_replace),to_delete
        ]

    def _create_colection_and_verifyit(self, collection: str, data: list, key: str):

        self.client.collection(collection)
        for d in data:
            self.client.create(d)
        for d in self.workers_data:
            self.assertEqual(d, self.client.get(d[key]), 'Error while trying to get {} object'.format(d))

    def test_single_client(self):

        self._create_colection_and_verifyit('workers',self.workers_data, '_key')
        self._create_colection_and_verifyit('cities', self.cities_data, '_key')

        for i in range(len(self.operational_objects)-1):
            self._check_simple_func(self.operators_fun[i],self.operational_objects[i])

        self._check_delete(self.operational_objects[-1])

        self.assertEqual(self.client.current_collection(),'cities')

        self.client.drop_collection('cities')
        self.assertFalse(self.client.collection_exists('cities'))

        self.assertTrue(self.client.collection_exists('workers'))
        self.client.collection('workers')

        self.client.drop_collection('workers')
        self.assertFalse(self.client.collection_exists('workers'))

    def _check_delete(self, key):
        self.client.delete(key)
        try:
            self.client.get(key)
            self.assertTrue(False, 'Encontramos un objeto que ha sido borrado')
        except KeyError:
            pass

    def _check_simple_func(self,fun,obj):
        if obj is tuple:
            fun(*obj)
        else:
            fun(obj)
        self.assertEqual(self.client.get(obj['_key']),obj)

    def _pusher_client(self,client:Client,data:list):
        self.client = client
        # self._create_colection_and_verifyit('workers', self.workers_data, '_key')
        self._create_colection_and_verifyit('cities', self.cities_data, '_key')

        self.client.create(data[0])
        self.client.update(data[1]['_key'],data[1])
        self.client.replace(data[2]['_key'],data[2])
        self.client.delete(data[3])

    def _puller_client(self,client:Client,data:list):
        self.client = client

        self.assertTrue(self.client.collection_exists('cities'),'No existe el collection cities, y debería existir')

        #check create
        self.assertEqual(self.client.get(data[0]['_key']), data[0],'Fallo en el create')

        #check update
        self.assertEqual(self.client.get(data[1]['_key']),data[1],'Fallo en el update')

        #check replace
        self.assertEqual(self.client.get(data[2]['_key']),data[1],'Fallo en el replace')

        try:
            self.client.get(data[3])
            assert True, 'Fallo en el delete'
        except KeyError:
            pass

    def test_clients_testers(self):
        puller_client = Client(SERVER_URL)
        pusher_client = Client(SERVER_URL)

        # el orden de los datos seguirá el orden de las operaciones
        # estas son:
        # 1-create 2-update 3-replace 4-delete
        data = [
            {'_key': 10, 'Name':'bla1'},
            {'_key': 2, 'Name':'bla2'},
            {'_key': 3, 'Name': 'bla3'},
            4
        ]
        p1 = Process(target=self._pusher_client,args=(pusher_client,data,))
        p2 = Process(target=self._puller_client, args=(puller_client, data,))

        p1.run()
        p1.join(timeout=10)
        p2.run()
        p2.join(timeout=10)