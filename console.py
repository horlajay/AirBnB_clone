#!/usr/bin/python3
"""
Console Module
"""
import re
import shlex
import ast
import cmd
from models import storage
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class console
    """
    prompt = "(hbnb) "

     def do_create(self, line):
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        instance = globals()[class_name]()
        instance.save()
        print(instance.id)

    def do_show(self, line):
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        instance_id = args[1]
        instances = storage.all(class_name)
        for instance in instances:
            if instance.id == instance_id:
                print(instance)
                return
        print("** no instance found **")

    def do_destroy(self, line):
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        instance_id = args[1]
        instances = storage.all(class_name)
        for instance in instances:
            if instance.id == instance_id:
                storage.delete(instance)
                storage.save()
                return
        print("** no instance found **")

    def do_all(self, line):
        args = line.split()
        if len(args) == 0:
            instances = storage.all()
        else:
            class_name = args[0]
            if class_name not in globals():
                print("** class doesn't exist **")
                return
            instances = storage.all(class_name)
        print([str(instance) for instance in instances])

    def do_update(self, line):
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        instance_id = args[1]
        instances = storage.all(class_name)
        for instance in instances:
            if instance.id == instance_id:
                if len(args) == 2:
                    print("** attribute name missing **")
                    return
                attribute_name = args[2]
                if len(args) == 3:
                    print("** value missing **")
                    return
                attribute_value = args[3]
                setattr(instance, attribute_name, attribute_value)
                storage.save()
                return
        print("** no instance found **")

    
    def do_quit(self, arg):
        """
        Quit command for  exit of  the program.
        """
        return True

    def do_EOF(self, arg):
        """
        EOF (Ctrl+D) a  signal for  exiting the program.
        """
        return True

    def emptyline(self):
        """
        Does nothing when an empty line is entered.
        """
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
