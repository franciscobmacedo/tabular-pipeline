# Data pipeline

Data pipeline to ingest, conform, normalise, validate and export tabular data files (for now) given yml schema(s) as the only source of truth.
It should be possible to easily plug it in modern orchestration tools such as Airflow and Dagster.

> :warning: This is a work in progress


## Steps

- [x] Read - currently csv and xlsx
- [x] Conform - detect column headers, normalise (according to schema rules/accepted aliases) and ignore irrelevant ones
- [ ] Normalise - normalise columns content according to schema data types
    - [ ] define accepted data formats (int, float, str, date, year-month, categorical)
    - [ ] allow schemas to extend said formats

## TODO
- [ ] Try this with airflow - use S3 operator to store data in between
- [ ] Try this with dagster ?
- [ ] Try this with pyodide ?
- [ ] make it work for multiple datasets - many files and many tables within each file
- [ ] allow other export formats - for now, data is transfered over csv, but we might want to use binary, like feather (which might require the usage of pandas)
- [ ] try with external data sources (like S3 bucket) - one should able to read and write from theme easily
- [ ] return data directly - it might be the case that there's no need to store the data between steps - in that case it should be returned directly.