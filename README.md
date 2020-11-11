# validateJSON [![Actions Status](https://github.com/abmamo/validateJSON/workflows/validateJSON/badge.svg)](https://github.com/abmamo/validateJSON/actions)
package to validate JSON data against a schema

the data schema consists of:
    - expected_keys: list of dicts describing the types & names
                     of each JSON parameter that MUST be in the
                     JSON object
    - conditional_keys: list of dicts describing the type, name
                        and dependence info of a set of each JSON
                        parameter that MUST be in the JSON
                        object
    - expected_keys: list of dicts describing the types & names
                     of each JSON parameter that may or may not
                     be in the JSON object
# quickstart
1. clone repo
```
git clone https://github.com/abmamo/validateJSON
```
2. install package
```
pip3 install /path/to/validateJSON
```
