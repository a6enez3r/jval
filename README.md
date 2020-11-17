# validateJSON ![build](https://github.com/abmamo/validateJSON/workflows/build/badge.svg?branch=main)
package to validate JSON data against a schema

# quickstart
clone repo
```
git clone https://github.com/abmamo/validateJSON
```
install package
```
pip3 install /path/to/validateJSON
```
define data schema (sample data schema below)
```
# sample JSON data
request_data = {
    "source_type": "local",
    "source_info": {
        "file_path": "<file path here>",
        "dir_path": "<some container name here>"
    },
    "store_type": "pg",
    "store_info": {
        "host": "localhost",
        "dbname": "postgres",
        "user": "abmamo",
        "password": "testpassword",
        "port": 5432
    }
}
# expected parameters / data schema
expected = [
    # store type
    {
        "param_name": "store_type",
        "param_type": str,
        "possible_values": ["pg", "mysql"]
    },
    # store info
    {
        "param_name": "store_info",
        "param_type": dict,
        "expected_keys": [
            {"param_name": "host", "param_type": str},
            {"param_name": "dbname", "param_type": str},
            {"param_name": "user", "param_type": str},
            {"param_name": "password", "param_type": str},
            {"param_name": "port", "param_type": int}
        ]
    },
    # source type
    {
        "param_name": "source_type",
        "param_type": str,
        "possible_values": ["local", "azure_storage"]
    },
    # source info
    {
        "param_name": "source_info",
        "param_type": dict,
        "conditional_keys": {
            "depends_on": "source_type",
            "dependence_info": {
                "local": {
                    "expected_keys": [
                        {"param_name": "file_path", "param_type": str}
                    ],
                    "optional_keys": [
                        {"param_name": "dir_path", "param_type": str},
                    ]
                },
                "azure_storage": {
                    "expected_keys": [
                        {"param_name": "connection_string", "param_type": str},
                        {"param_name": "container_name", "param_type": str},
                    ],
                    "optional_keys": [
                        {"param_name": "file_name", "param_type": str}
                    ]
                }
            }  
        }
    },
]
optional = [
    {
        "param_name": "time_limit",
        "param_type": int
    }
]
```
run validator
```
from validateJSON import JSONValidator
# init validator
v = JSONValidator()
# pass test data
validated = v.validate(
    json_object=request_data,
    expected_keys=expected,
    optional_keys=optional
)
```
# validation

validate JSON data against a data schema. a data schema is made
up of expected_keys (describing each parameter the JSON object must have) 
& optional_keys (describing parameters that may or may not be in JSON object) 

expected keys: is a list of keys (which are python dict objects)
               describing the required parameters of a JSON object

               keys: are python dicts which contain info about
                     parameters of a JSON object

                     required_params:
                        "param_name": name of parameter
                        "param_type": type of parameter
                     
                     optional_params:
                        "possible_values": values a parameter can be
                        "expected_keys": nested expected parameters
                        "conditional_keys": parameters whose names and
                                            values depend on another parameter

```
# simple
simple_key_one =
{
    "param_name": "source_type",
    "param_type": str,
    "possible_values": ["local", "azure_storage"]
}
simple_key_two =
{
    "param_name": "source_type",
    "param_type": str
}
# nested
nested_key =
{
    "param_name": "store_info",
    "param_type": dict,
    "expected_keys": [
        {"param_name": "host", "param_type": str},
        {"param_name": "dbname", "param_type": str},
        {"param_name": "user", "param_type": str},
        {"param_name": "password", "param_type": str},
        {"param_name": "port", "param_type": int}
    ]
}
# conditional
conditional_key =
{
    "param_name": "source_info",
    "param_type": dict,
    "conditional_keys": {
        "depends_on": "source_type",
        "dependence_info": {
            # value of depends_on
            "local": {
                # expected keys based on that value
                "expected_keys": [
                    {"param_name": "file_path", "param_type": str}
                ],
                # optional keys based on that value
                "optional_keys": [
                    {"param_name": "dir_path", "param_type": str},
                ]
            },
            "azure_storage": {
                "expected_keys": [
                    {"param_name": "connection_string", "param_type": str},
                    {"param_name": "container_name", "param_type": str},
                ],
                "optional_keys": [
                    {"param_name": "file_name", "param_type": str}
                ]
            }
        }
    }
}
```
- optional_keys: list of dicts describing the types & names
                    of each JSON parameter that may or may not
                    be in the JSON object (only checked for types)
```
# simple
simple_key_one =
{
    "param_name": "source_type",
    "param_type": str
}
```