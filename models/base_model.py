#!/usr/bin/python3
''' 
module for BaseModel class 
'''

#libraries
from datetime import datetime
from uuid import uuid4
from . import storage

ISOFORMAT = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    ''' class of the base model that everyhting else is inheriting from'''
    def __init__(self, *args, **kwargs):
        if kwargs:
            for k in kwargs:
                if k in ['created_at', 'updated_at']:
                    setattr(self, k, datetime.strptime(kwargs[k], ISOFORMAT))
                elif k != '__class__':
                    setattr(self, k, kwargs[k])

        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at.replace()
            storage.new(self)
        
    def save(self):
        '''
        updates the public instance attribute updated_at with the current datetime 
        and should save the model, I don't know why they asked us to call it save
        we might probably update this later
        '''
        self.updated_at=datetime.utcnow()
        storage.save()

    def to_dict(self):
        '''
        returns a dictionary containing all keys/values of __dict__ of the model
        '''
        dct= self.__dict__.copy()
        dct['__class__'] = self.__class__.__name__
        dct['created_at'] = self.created_at.isoformat()
        dct['updated_at'] = self.updated_at.isoformat()
        return dct

    def __str__(self):
        '''
        returns a string representation of the model when an instance is created
        '''
        return '[{}] [{}] {}'.format(self.__class__.__name__, self.id, self.__dict__)
