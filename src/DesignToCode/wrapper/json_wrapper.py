import json
from dataclasses import dataclass
from typing import Optional, Type, Any, Dict

from pydantic import BaseModel, ValidationError


@dataclass
class JsonWrapper:
    """
    A utility class for reading JSON files.
    """
    # json_file_path: str
    # json_source: Optional[str] = None  # Can be a file path or a JSON string
    # from_string: bool = False  # Indicates if json_source is a string

    def read(self, json_source, from_string: bool = False) -> Dict[str, Any]:
        """
        Reads JSON data from a file or string and returns it as a dictionary.

        :return: A dictionary representation of the JSON data.
        """
        try:
            if from_string:
                data = json.loads(json_source)
            else:
                with open(json_source, "r", encoding="utf-8") as f:
                    data = json.load(f)

            return data

        except (FileNotFoundError, json.JSONDecodeError, ValidationError) as e:
            print(f"Error reading or validating JSON data: {e}")
            return {}



    def read_to_pydantic(self, model: Optional[Type[BaseModel]] = None) -> BaseModel:
        """
        Reads a JSON file and returns its content as a dictionary or as an instance of a Pydantic model.

        :param model: Optional Pydantic model class to parse the JSON data into.
        :return: A dictionary or a Pydantic model instance.
        """
        try:
            with open(self.json_source, "r", encoding="utf-8") as f:
                data = json.load(f)
            if model:
                return model(**data)
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading JSON file: {e}")
            return {}
        except ValidationError as e:
            print(f"Error validating JSON data: {e}")
            raise



        # # Reading JSON from a file
        # json_wrapper = JsonWrapper(json_source="data.json")
        # data = json_wrapper.read()
        # print(data)
        #
        # # Reading JSON from a string
        # json_string = '{"prompt": "Hello, Mistral AI!", "max_tokens": 100}'
        # json_wrapper = JsonWrapper(json_source=json_string, from_string=True)
        # data = json_wrapper.read()
        # print(data)


        #to pydantic
        # # Define a Pydantic model
        # class ConfigData(BaseModel):
        #     setting_a: str
        #     setting_b: int
        #
        # # Parse JSON data into the model
        # json_wrapper = JsonWrapper(json_source="config.json")
        # try:
        #     config = json_wrapper.parse(model=ConfigData)
        #     print(config.setting_a, config.setting_b)
        # except ValidationError as e:
        #     print(f"Invalid config data: {e}")