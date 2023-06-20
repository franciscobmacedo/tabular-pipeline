import csv
import json
from typing import Iterable, Literal, Type

import yaml
from pydantic import AliasChoices, BaseModel
from thefuzz import fuzz

from schemas.base import Address, ApprovisionDetailOffRoll, SpringSchoolCensusDataset
from schemas.export import dump_schema

MIN_SCORE = 80


def dump_schema(format: Literal["json", "yaml"], schema: Type[BaseModel]):
    name = schema.model_config.get("title", "schema")
    if format == "json":
        with open(f"schemas/{name}.json", "w") as f:
            return json.dump(schema.model_json_schema(), f, indent=2)
    elif format == "yaml":
        with open(f"schemas/{name}.yml", "w") as f:
            return yaml.dump(schema.model_json_schema(), f)


def normalise_entry(entry) -> str:
    return str(entry).lower().strip()


def detect_fields(keys: Iterable, schema: Type[BaseModel]):
    """detect data fields given the original keys/headers and the expected schema"""
    model_fields = schema.model_fields
    matched_fields = []
    for field_key, field_info in model_fields.items():
        field_choices = [field_key]
        if field_info.validation_alias and isinstance(
            field_info.validation_alias, AliasChoices
        ):
            field_choices.extend(field_info.validation_alias.choices)
        for key in keys:
            normalised_key = normalise_entry(key)
            for field_choice in field_choices:
                score = fuzz.partial_ratio(field_choice, normalised_key)
                if score >= MIN_SCORE:  # Adjust the threshold as per your needs
                    matched_fields.append((field_key, key, score))
    return matched_fields


def conform(record: list[dict], schema: Type[BaseModel]) -> list[dict]:
    """
    return the data in the same format as the input.
    As an example, it's a list of dicts but it can be a stream of events as well.
    """
    matched_fields = detect_fields(record[0].keys(), schema)
    return [{field: entry[key] for field, key, _ in matched_fields} for entry in record]


def run_pipeline(path: str, schema: Type[BaseModel]):
    # dummy read step
    with open(path, "r") as f:
        data = [row for row in csv.DictReader(f, skipinitialspace=True)]

    # conform data to match model
    conformed_data = conform(data, schema)
    print(conformed_data)


if __name__ == "__main__":
    # dump schemas to json and uaml
    dump_schema("json", Address)
    dump_schema("yaml", SpringSchoolCensusDataset)

    # conform addresses values
    run_pipeline("samples/addresses.csv", Address)
    run_pipeline("samples/approvisiondetailoffroll.csv", ApprovisionDetailOffRoll)
