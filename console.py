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
