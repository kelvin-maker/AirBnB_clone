#!/usr/bin/python3
"""
Provides the 'models' package
"""
import models

from . import base_model


def getmodel(name):
    """
    Get a model by name
    """
    for item in dir(models):
        attr = getattr(models, item)
        if type(attr) is type(models) and name in dir(attr):
            match = getattr(attr, name)
            if type(match) is type:
                return (match)
    return None



