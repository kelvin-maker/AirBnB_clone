#!/usr/bin/python3
"""
console main file
"""
import models
from cmd import Cmd


class HBNBCommand(Cmd):
    """condole characteristics and commands"""
    prompt = "(hbnb)"



if __name__ == '__main__':
    HBNBCommand().cmdloop()

