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

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            new_instance = self.classes[args[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            instance = storage.all().get(key)
            if instance is None:
                print("** no instance found **")
            else:
                print(instance)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances based or not on the class name."""
        args = arg.split()
        if not args:
            instances = storage.all().values()
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        else:
            instances = [str(obj) for key, obj in storage.all().items() if key.startswith(args[0])]
        print([str(instance) for instance in instances])

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or updating attribute."""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            instance = storage.all().get(key)
            if instance is None:
                print("** no instance found **")
            else:
                attr_name = args[2]
                attr_value = args[3].strip('"')
                if hasattr(instance, attr_name):
                    attr_type = type(getattr(instance, attr_name))
                    attr_value = attr_type(attr_value)
                setattr(instance, attr_name, attr_value)
                instance.save()

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
