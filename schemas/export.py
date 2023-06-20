import json
from typing import Literal, Type

import yaml
from pydantic import BaseModel


def dump_schema(format: Literal["json", "yaml"], schema: Type[BaseModel]):
    name = schema.model_config.get("title", "schema")
    if format == "json":
        with open(f"schemas/{name}.json", "w") as f:
            return json.dump(schema.model_json_schema(), f, indent=2)
    elif format == "yaml":
        with open(f"schemas/{name}.yml", "w") as f:
            return yaml.dump(schema.model_json_schema(), f)
