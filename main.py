import typer

from tabular_pipeline import standardise


def main(file: str, schema: str):
    standardise(data_file_path=file, schema_file_path=schema)


if __name__ == "__main__":
    typer.run(main)
