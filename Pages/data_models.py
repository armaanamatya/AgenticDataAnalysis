from dataclasses import dataclass
import os

@dataclass
class InputData:
    variable_name: str
    data_path: str
    data_description: str
    