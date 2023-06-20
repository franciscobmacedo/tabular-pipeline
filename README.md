# Dummy branch for pipeline for school census data

Using the [default schema](./default_school_census.yml), this draft tries to implement a conform step based on pydantic schema.

The idea is to try and determine why Pydantic based schemas can be a good idea:


- Custom fields - for example, `postcode` can be a custom field that derives from str. If we have a repo for our common datasets, we can have common fields as well - [See the postcode example here](./schemas/fields.py).
- allows to export the schema to json (and, with minor adaptation, to yaml) - we can maybe adapt the ERD generator for this? [See the example here](./schemas/export.py). It follows the standards.
- One can choose between strict field conversion or not (in V2).
- most common field constrains/validation rules are already builtin in pydantic:
  -  enums (for choice fields)
  -  numeric constrains (`gt`, `lt`, etc..)
  -  string constrains (`min_length`, `max_length`, regular expressions, etc...)
- validation between fields is also possible and directly integrated with the class. We can then split the code across different files, if it gets to big or not use this feature at all.


However, pydantic V2 (which allows multiple aliases and toggling between field strict mode or not) is still in beta - but they claim that [it's ready for migration](https://docs.pydantic.dev/dev-v2/migration/).



