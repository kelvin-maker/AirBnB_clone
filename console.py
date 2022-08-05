#!/usr/bin/python3
"""
console main file
"""
import cmd
#from cmd import Cmd
import models
import sys
import shlex
import re
import ast
from models.__init__ import storage

class HBNBCommand(cmd.Cmd):
    """condole characteristics and commands"""
    prompt = "(hbnb)"

    def console_create(self, arg):
        ''' creates a new instance of the class passed as argument
            and saves it to the json storage file
        '''
        if not arg:
            print("** class name missing **")
            return
        elif arg not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[arg]()
        storage.save()
        print(new_instance.id)

    def help_create(self):
        """ prints Documentation for the create command """
        print("creates a new instance of the class passed as argument")
        print("[Usage]: create <className>\n")

    def console_show(self, arg):
        ''' prints the string representation of an instance
            based on the class name and id
        '''
        args = shlex.split(arg)

        if len(args) >= 1:
            cls = args[0]
        else:
            print("** class name missing **")
            return
        if cls not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) >= 2:
            id = args[1]
        else:
            print("** instance id missing **")
            return

        key = cls + '.' + id
        all = storage.all()
        if key not in all:
            print("** no instance found **")
            return
        print(all[key])

    def help_show(self):
        """ prints documentation for the show command """
        print("prints the string representation of an instance")
        print("[Usage]: show <className> <objectId>\n")

    def console_destroy(self, arg):
        ''' Deletes an instance based on the class name and id
            and saves the change into the JSON Storage file
        '''
        args = shlex.split(arg)

        if len(args) >= 1:
            cls = args[0]
        else:
            print("** class name missing **")
            return
        if cls not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) >= 2:
            id = args[1]
        else:
            print("** instance id missing **")
            return

        key = cls + '.' + id
        all = storage.all()
        if key not in all:
            print("** no instance found **")
            return

        del (all[key])
        storage.save()

    def help_destroy(self):
        ''' prints documentaion for the destroy command '''
        print("Deletes an instance based on the class name and id")
        print("[Usage]: destroy <className> <objectId>\n")

    def console_all(self, arg):
        ''' Prints all string representation of all instances
            based or not on the class name.
        '''
        arg = arg.strip("\"'")
        result = []
        all = storage.all()
        if not arg:
            for key in all.keys():
                result.append(all[key].__str__())
            print(result)
            return

        for key in all.keys():
            if key.find(arg) != -1 and arg in self.classes:
                result.append(all[key].__str__())
        if len(result) <= 0 and arg not in self.classes:
            print("** class doesn't exist **")
            return
        print(result)

    def help_all(self):
        ''' prints documentaion for the all command '''
        print("Prints all string representation of all instances")
        print("based or not on the class name")
        print("[Usage]: all <className>\n")

    def console_update(self, arg):
        '''  Updates an instance based on the class name
            and id by adding or updating attribute and saves
            the change into the JSON Storage file
        '''
        args = shlex.split(arg)
        cls = id = attr = val = ''

        if len(args) >= 1:
            cls = args[0]
        else:
            print("** class name missing **")
            return
        if cls not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) >= 2:
            id = args[1]
        else:
            print("** instance id missing **")
            return
        key = cls + '.' + id
        if key not in storage.all():
            print("** no instance found **")
            return

        arg_section = ''
        if len(args) >= 3:
            arg_section = arg.split(None, 2)[2]
            evaled_args = ''
            try:
                evaled_args = ast.literal_eval(arg_section)
            except (SyntaxError, ValueError, AssertionError):
                pass

            if isinstance(evaled_args, dict):
                arg_section = evaled_args
            else:
                attr = args[2]
        else:
            print("** attribute name missing **")
            return
        if len(args) >= 4:
            if not isinstance(arg_section, dict):
                val = args[3]
        else:
            print("** value missing **")
            return

        obj = storage.all()[key]
        if isinstance(arg_section, dict):
            # type cast the value depends on the attribute
            for key in arg_section.keys():
                if key in self.attr_types:
                    arg_section[key] = self.attr_types[key](arg_section[key])
            # update the object attributes dictionary
            obj.__dict__.update(arg_section)
        else:
            # type cast the value depends on the attribute
            if attr in self.attr_types:
                val = self.attr_types[attr](val)
            new_attr = {attr: val}
            # update the object attributes dictionary
            obj.__dict__.update(new_attr)
        obj.save()

    def help_update(self):
        """ prints Documentation for the update command """
        print("Updates an object's attributes")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == '__main__':
    HBNBCommand().cmdloop()

