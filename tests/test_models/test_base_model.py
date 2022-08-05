#!/usr/bin/python3

#please look through the unitest again; I was already stressed when i did this

''' 
module for base_model tests 
'''

from unittest import TestCase
import json
import re
from uuid import UUID, uuid4
from datetime import datetime
from time import sleep
from models.base_model import BaseModel

class TestBaseModel(TestCase):
    ''' tests BaseModel class '''
    def test_0(self):
        ''' task 0 tests '''
        obj = BaseModel()

        # id format and uniqueness
        self.assertTrue(type(getattr(obj, 'id', None) is str) and
                        UUID(obj.id))
        self.assertNotEqual(BaseModel().id, obj.id)
        self.assertNotEqual(BaseModel().id, BaseModel().id)
        self.assertNotEqual(BaseModel().id, BaseModel().id)

        # created_at and updated_at types
        self.assertTrue(type(obj.created_at) is datetime)
        self.assertTrue(type(obj.updated_at) is datetime)

        # string representation
        self.assertEqual(str(obj), '[{}] ({}) {}'.format(
            'BaseModel', obj.id, obj.__dict__))

        # time updates
        old_ctm = obj.created_at
        old_utm = obj.updated_at
        sleep(0.01)
        obj.save()
        self.assertEqual(old_ctm, obj.created_at)
        self.assertNotEqual(old_utm, obj.updated_at)

        old_ctm = obj.created_at
        old_utm = obj.updated_at
        sleep(0.01)
        obj.save()
        self.assertEqual(old_ctm, obj.created_at)
        self.assertNotEqual(old_utm, obj.updated_at)

        self.assertEqual(obj.to_dict(),
                         {'__class__': 'BaseModel', 'id': obj.id,
                          'created_at': obj.created_at.isoformat(),
                          'updated_at': obj.updated_at.isoformat()})
        now = datetime.utcnow()
        obj_dict = {'id': str(uuid4()), 'created_at': now.isoformat(),
                    'updated_at': now.isoformat(), '__class__': 'BaseModel'}
        
        # same objects creation
        self.assertEqual(obj.to_dict(), BaseModel(**obj_dict).to_dict())
        self.assertEqual(str(obj), str(BaseModel(**obj_dict)))

        # no __class__ dependency
        del obj_dict['__class__']
        BaseModel(**obj_dict)  # no execption raised

        ##
        # normal creation in kwargs absence
        obj = BaseModel()
        self.assertTrue(type(getattr(obj, 'id', None) is str) and
                        UUID(obj.id))
        self.assertNotEqual(BaseModel().id, obj.id)
        self.assertNotEqual(BaseModel().id, BaseModel().id)
        self.assertNotEqual(BaseModel().id, BaseModel().id)

        # time updates
        old_ctm = obj.created_at
        old_utm = obj.updated_at
        sleep(0.01)
        obj.save()
        self.assertEqual(old_ctm, obj.created_at)
        self.assertNotEqual(old_utm, obj.updated_at)

        old_ctm = obj.created_at
        old_utm = obj.updated_at
        sleep(0.01)
        obj.save()
        self.assertEqual(old_ctm, obj.created_at)
        self.assertNotEqual(old_utm, obj.updated_at)