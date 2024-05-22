#!/usr/bin/python3
"""
Module for serializing and deserializing data
"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


class FileStorage:
    """
    FileStorage class for storing, serializing and deserializing data
    """
    _file_path = "file.json"
    __objects = {}

    def add(self, obj):
        """
        Adds an object to the __objects dictionary with a key
        formatted as <obj class name>.id.
        """
        class_name = obj.__class__.__name__
        key = f"{class_name}.{obj.id}"
        FileStorage.__objects[key] = obj

    def get_all(self):
        """
        Returns the __objects dictionary, providing access to all stored objects.
        """
        return FileStorage.__objects

    def save_to_file(self):
        """
        Serializes the __objects dictionary into JSON format
        and writes it to the file specified by _file_path.
        """
        object_dict = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage._file_path, "w", encoding="utf-8") as file:
            json.dump(object_dict, file)

    def reload(self):
        """
        Deserializes the JSON file specified by _file_path.
        """
        if os.path.isfile(FileStorage._file_path):
            with open(FileStorage._file_path, "r", encoding="utf-8") as file:
                try:
                    obj_dict = json.load(file)
                    for key, value in obj_dict.items():
                        class_name, obj_id = key.split('.')
                        cls = eval(class_name)
                        instance = cls(**value)
                        FileStorage.__objects[key] = instance
                except Exception:
                    pass
