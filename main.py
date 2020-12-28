import json
import clipboard


class JsonToBean:
    bean_name = None
    config = None
    json_response = None
    class_properties = str()
    class_getters_setters = str()
    java_class = str()
    has_get_set = None

    def __init__(self):
        self.get_config()

    def start(self):
        self.get_bean_name()
        self.will_generate_get_set()
        self.get_json_response()
        self.generate_bean()
        self.copy_to_clipboard()

    # config.json contains type for collection (Array) in java equivalent, Ex. java.util.List (List)
    def get_config(self):
        try:
            with open('config.json') as json_file:
                self.config = json.load(json_file)
        except:
            self.config = {
                "collection": "List"
            }

    def get_bean_name(self):
        self.bean_name = input("Bean name: ")
        self.bean_name = self.bean_name[0].capitalize() + self.bean_name[1:]
        if len(self.bean_name) == 0:
            print("Bean name cant be null")
            self.get_bean_name()

    def will_generate_get_set(self):
        answer = input("Generate getters and setters? (y/n) ")
        self.has_get_set = True if answer.lower() == 'y' else False

    def get_json_response(self):
        input("Press enter if you already copied the json.")
        try:
            self.json_response = json.loads(clipboard.paste())
        except:
            print("Your json might be invalid!")
            self.get_json_response()

    def create_properties_and_getters_setters(self):
        for key, value in self.json_response.items():
            key_cap = key.capitalize()
            not_string_type = f"{self.config['collection']}<Insert{key[0].capitalize() + key[1:]}TypeHere>" if type(
                value) is list else f"Insert{key_cap}TypeHere"
            data_type = 'String' if type(value) is str or type(
                value) is int else not_string_type
            self.__add_property(data_type, key)
            if self.has_get_set:
                self.__add_getter_setter(data_type, key)

    def __add_getter_setter(self, data_type, key):
        self.class_getters_setters += f"\tpublic {data_type} get{key[0].capitalize() + key[1:]}(){{\n\t\treturn {key};\n\t}}\n\n"
        self.class_getters_setters += f"\tpublic void set{key[0].capitalize() + key[1:]}({data_type} {key}){{\n\t\tthis.{key} = {key};\n\t}}\n\n"

    def __add_property(self, data_type, key):
        self.class_properties += f"\tprivate {data_type} {key};\n"

    def generate_bean(self):
        self.create_properties_and_getters_setters()
        self.java_class = f'public class {self.bean_name} {{\n{self.class_properties}\n{self.class_getters_setters}}}'

    def copy_to_clipboard(self):
        try:
            clipboard.copy(self.java_class)
        finally:
            print("The java class is copied to clipboard successfully.")
