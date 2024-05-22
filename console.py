#!/usr/bin/python
"""
Console module for the HBNB project.
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


def split_curly_braces(e_arg):
    """
    Splits the curly braces for the update method.
    """
    curly_braces = re.search(r"\{(.*?)\}", e_arg)

    if curly_braces:
        id_with_comma = shlex.split(e_arg[:curly_braces.span()[0]])
        id = [i.strip(",") for i in id_with_comma][0]

        str_data = curly_braces.group(1)
        try:
            arg_dict = ast.literal_eval("{" + str_data + "}")
        except Exception:
            print("**  invalid dictionary format **")
            return
        return id, arg_dict
    else:
        commands = e_arg.split(",")
        if commands:
            try:
                id = commands[0]
            except Exception:
                return "", ""
            try:
                attr_name = commands[1]
            except Exception:
                return id, ""
            try:
                attr_value = commands[2]
            except Exception:
                return id, attr_name
            return f"{id}", f"{attr_name} {attr_value}"


class HBNBConsole(cmd.Cmd):
    """
    Command interpreter class for HBNB.
    """
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "Amenity", "Place", "Review", "State", "City"]

    def emptyline(self):
        """
        Override the emptyline method to do nothing.
        """
        pass

    def do_EOF(self, arg):
        """
        Handle the EOF (Ctrl+D) signal to exit the program.
        """
        return True

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_create(self, arg):
        """
        Create a new instance of a class and save it to the JSON file.
        Usage: create <class_name>
        """
        arguments = shlex.split(arg)

        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{arguments[0]}()")
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        arguments = shlex.split(arg)

        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(arguments[0], arguments[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        arguments = shlex.split(arg)

        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(arguments[0], arguments[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Print the string representation of all instances or a specific class.
        Usage: <class_name>.all()
        """
        objects = storage.all()
        arguments = shlex.split(arg)

        if len(arguments) == 0:
            for obj in objects.values():
                print(obj)
        elif arguments[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for obj in objects.values():
                if obj.__class__.__name__ == arguments[0]:
                    print(obj)

    def do_count(self, arg):
        """
        Count the number of instances of a class.
        Usage: <class_name>.count()
        """
        objects = storage.all()
        arguments = shlex.split(arg)

        if arg:
            class_name = arguments[0]

        count = 0

        if arguments:
            if class_name in self.valid_classes:
                for obj in objects.values():
                    if obj.__class__.__name__ == class_name:
                        count += 1
                print(count)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        arguments = shlex.split(arg)

        if len(arguments) == 0:
            print("** class name missing **")
        elif arguments[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(arguments) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(arguments[0], arguments[1])
            if key not in objects:
                print("** no instance found **")
            elif len(arguments) < 3:
                print("** attribute name missing **")
            elif len(arguments) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                curly_braces = re.search(r"\{(.*?)\}", arg)

                if curly_braces:
                    try:
                        str_data = curly_braces.group(1)
                        arg_dict = ast.literal_eval("{" + str_data + "}")
                        for attr_name, attr_value in arg_dict.items():
                            setattr(obj, attr_name, attr_value)
                    except Exception:
                        pass
                else:
                    attr_name = arguments[2]
                    attr_value = arguments[3]
                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)

                obj.save()

    def default(self, arg):
        """
        Handle unrecognized commands.
        """
        arg_list = arg.split('.')
        class_name = arg_list[0]
        command = arg_list[1].split('(')
        cmd_method = command[0]
        extra_args = command[1].split(')')[0]

        method_dict = {
            'all': self.do_all,
            'show': self.do_show,
            'destroy': self.do_destroy,
            'update': self.do_update,
            'count': self.do_count
        }

        if cmd_method in method_dict:
            if cmd_method != "update":
                return method_dict[cmd_method](f"{class_name} {extra_args}")
            else:
                if not class_name:
                    print("** class name missing **")
                    return
                try:
                    obj_id, arg_dict = split_curly_braces(extra_args)
                except Exception:
                    pass
                try:
                    call = method_dict[cmd_method]
                    return call(f"{class_name} {obj_id} {arg_dict}")
                except Exception:
                    pass
        else:
            print(f"*** Unknown syntax: {arg}")
            return False


if __name__ == '__main__':
    HBNBConsole().cmdloop()

