#!/usr/bin/python3
"""

"""

import json
import os
from models.base_model import BaseModel


class FileStorage:
    """

    """
    __file_path = "file.json"

    __objects = {}

    def new(self, obj):
        """

        """
        object_class_name = obj.__class__.__name__

        key = "{}.{}".format(object_class_name, obj.id)

        FileStorage.__objects[key] = obj


    def all(self):
        """

        """
        return FileStorage.__objects
    

    def save(self):
        """

        """
        alls_objts = FileStorage.__objects
        
        obj_dictionary = {}

        for obj in alls_objts.keys():
            obj_dictionary[obj] = alls_objts[obj].to_dict()

        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_dictionary, file)

    def reload(self):
        """

        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                try:
                    obj_dictionary = json.load(file)

                    for key, value in obj_dictionary.items():
                        cls_name, object_id = key.splt(".")
                        clas = eval(cls_name)

                        inatances = clas(**value)

                        FileStorage.__objects[key] = inatances
                except Exception:
                    pass

