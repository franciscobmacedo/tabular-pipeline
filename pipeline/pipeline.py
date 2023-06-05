import uuid

from pipeline.steps.conform import Conform
from pipeline.steps.load import Load
from pipeline.read import load_schema


def standardise(data_file_path: str, schema_file_path: str):
    session_id = uuid.uuid4()
    schema = load_schema(session_id, schema_file_path)

    loader = Load(session_id=session_id, file_path=data_file_path)
    conformer = Conform(session_id=session_id, schema=schema)
    # TODO - normaliser, validator

    loader.run()
    conformer.run()
    return conformer.dataset.export('xlsx')
