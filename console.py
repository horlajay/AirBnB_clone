#!/usr/bin/python3
"""
Console module
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


def parse_curly_braces(argument):
    """
    Parses curly braces for the update command.
    """
    curly_content = re.search(r"\{(.*?)\}", argument)
    if curly_content:
        base_cmd = shlex.split(argument[:curly_content.span()[0]])
        identifier = [item.strip(",") for item in base_cmd][0]
        dict_content = curly_content.group(1)
        try:
            parsed_dict = ast.literal_eval("{" + dict_content + "}")
        except Exception:
            print("** invalid dictionary format **")
            return
        return identifier, parsed_dict
    else:
        split_args = argument.split(",")
        if split_args:
            try:
                identifier = split_args[0]
            except Exception:
                return "", ""
            try:
                attr_name = split_args[1]
            except Exception:
                return identifier, ""
            try:
                attr_value = split_args[2]
            except Exception:
                return identifier, attr_name
            return f"{identifier}", f"{attr_name} {attr_value}"


class HBNBCommand(cmd.Cmd):

    """
    Command interpreter class for HBNB
    """
    prompt = "(hbnb) "
    available_classes = ["BaseModel", "User", "Amenity",
                         "Place", "Review", "State", "City"]

    def emptyline(self):
        """
        Ignore empty lines.
        """
        pass

    def do_EOF(self, line):
        """
        Exit the command interpreter.
        """
        return True

    def do_quit(self, line):
        """
        Quit command to exit the interpreter.
        """
        return True

    def do_create(self, args):
        """
        Create a new instance of BaseModel, save it, and print the id.
        Usage: create <class_name>
        """
        tokens = shlex.split(args)
        if not tokens:
            print("** class name missing **")
        elif tokens[0] not in self.available_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{tokens[0]}()")
            new_instance.save()
            print(new_instance.id)

    def do_show(self, args):
        """
        Show string representation of an instance based on class name and id.
        Usage: show <class_name> <id>
        """
        tokens = shlex.split(args)
        if not tokens:
            print("** class name missing **")
        elif tokens[0] not in self.available_classes:
            print("** class doesn't exist **")
        elif len(tokens) < 2:
            print("** instance id missing **")
        else:
            obj_key = "{}.{}".format(tokens[0], tokens[1])
            if obj_key in storage.all():
                print(storage.all()[obj_key])
            else:
                print("** no instance found **")

    def do_destroy(self, args):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        tokens = shlex.split(args)
        if not tokens:
            print("** class name missing **")
        elif tokens[0] not in self.available_classes:
            print("** class doesn't exist **")
        elif len(tokens) < 2:
            print("** instance id missing **")
        else:
            obj_key = "{}.{}".format(tokens[0], tokens[1])
            if obj_key in storage.all():
                del storage.all()[obj_key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, args):
        """
        Print all string representations of all instances or a specific class.
        Usage: all or all <class_name>
        """
        tokens = shlex.split(args)
        if not tokens:
            for obj in storage.all().values():
                print(obj)
        elif tokens[0] not in self.available_classes:
            print("** class doesn't exist **")
        else:
            for obj in storage.all().values():
                if obj.__class__.__name__ == tokens[0]:
                    print(obj)

    def do_count(self, args):
        """
        Count the number of instances of a specific class.
        Usage: <class name>.count()
        """
        tokens = shlex.split(args)
        if not tokens:
            print("** class name missing **")
        elif tokens[0] in self.available_classes:
            count = sum(1 for obj in storage.all().values()
                        if obj.__class__.__name__ == tokens[0])
            print(count)
        else:
            print("** class doesn't exist **")

    def do_update(self, args):
        """
        Update an instance by adding or updating attributes.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        tokens = shlex.split(args)
        if not tokens:
            print("** class name missing **")
        elif tokens[0] not in self.available_classes:
            print("** class doesn't exist **")
        elif len(tokens) < 2:
            print("** instance id missing **")
        else:
            obj_key = "{}.{}".format(tokens[0], tokens[1])
            if obj_key not in storage.all():
                print("** no instance found **")
            elif len(tokens) < 3:
                print("** attribute name missing **")
            elif len(tokens) < 4:
                print("** value missing **")
            else:
                obj = storage.all()[obj_key]
                curly_content = re.search(r"\{(.*?)\}", args)
                if curly_content:
                    try:
                        dict_content = curly_content.group(1)
                        parsed_dict = ast.literal_eval("{"
                                                        + dict_content + "}")
                        for key, value in parsed_dict.items():
                            setattr(obj, key, value)
                    except Exception:
                        pass
                else:
                    attr_name = tokens[2]
                    attr_value = tokens[3]
                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)
                obj.save()

    def default(self, line):
        """
        Handle default behavior for unrecognized commands.
        """
        cls_cmd = line.split('.')
        if len(cls_cmd) < 2:
            print("*** Unknown syntax: {}".format(line))
            return False
        class_name, method_call = cls_cmd[0], cls_cmd[1]
        if class_name not in self.available_classes:
            print("** class doesn't exist **")
            return False
        method_name = method_call.split('(')[0]
        args = method_call.split('(')[1].split(')')[0]
        if method_name == "all":
            self.do_all(class_name)
        elif method_name == "count":
            self.do_count(class_name)
        elif method_name == "show":
            self.do_show(f"{class_name} {args}")
        elif method_name == "destroy":
            self.do_destroy(f"{class_name} {args}")
        elif method_name == "update":
            obj_id, updates = parse_curly_braces(args)
            for key, value in updates.items():
                self.do_update(f"{class_name} {obj_id} {key} {value}")
        else:
            print("*** Unknown syntax: {}".format(line))
            return False


if __name__ == '__main__':
    HBNBCommandInterpreter().cmdloop()
