from tabular_pipeline import standardise


def main(file: str, schema: str):
    standardise(schema=schema, file_path=file)


if __name__ == "__main__":
    main(
        "samples/files/sample1.xslx",
        "samples/schemas/sample1.yml",
    )
