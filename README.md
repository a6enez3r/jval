# jval ![test](https://github.com/abmamo/jval/workflows/test/badge.svg?branch=main)
package to validate JSON data against a schema

# quickstart
create virtualenv
```
  python3 -m venv env && source env/bin/activate && pip3 install --upgrade pip
```
install jval
```
  pip3 install jval @ https://github.com/abmamo/jval/archive/v0.0.1.tar.gz
```
sample JSON data
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
```
define data schema
```
# sample data schema
# expected parameters
expected = [
    # store type
    {
        "param_name": "store_type",
        "param_type": str,
        # store_type can only be "pg" or "mysql"
        "possible_values": ["pg", "mysql"]
    },
    # store info
    {
        "param_name": "store_info",
        "param_type": dict,
        # nested expected parameters
        "expected": [
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
        # source_type has to be either local or azure_storage
        "possible_values": ["local", "azure_storage"]
    },
    # source info
    {
        "param_name": "source_info",
        "param_type": dict,
        "conditional_keys": {
            "depends_on": "source_type",
            "dependence_info": {
                # if value of "source_type" is local
                "local": {
                    # we expect dir_path to be in JSON object
                    "expected": [
                        {"param_name": "dir_path", "param_type": str}
                    ],
                    # file_name may or may not be in JSON object
                    "optional": [
                        {"param_name": "file_name", "param_type": str},
                    ]
                },
                # if value of "source_type" is azure_storage
                "azure_storage": {
                    # we expect connection_string & container_name to be in JSON object
                    "expected": [
                        {"param_name": "connection_string", "param_type": str},
                        {"param_name": "container_name", "param_type": str},
                    ],
                    # file_name may or may not be in JSON object
                    "optional": [
                        {"param_name": "file_name", "param_type": str}
                    ]
                }
            }  
        }
    },
]
# optional parameters
optional = [
    {
        # if time_limit passed in JSON object
        "param_name": "time_limit",
        # it has to be an int
        "param_type": int
    }
]
```
run validator
```
from jval import JVal
# init validator
v = JVal()
# pass JSON & data schema to validator
validated = v.validate(
    json_object=request_data,
    expected=expected,
    optional=optional
)
```
if validated is True JSON data matches schema. 

by default logging level is set to `ERROR` to change this and see details on which parameters failed you can set up logger as:
```
import logging
from jval import logger as validator_logger
validator_logger.setLevel(logging.INFO)
from jval import JVal
# init validator
v = JVal()
# pass JSON & data schema to validator
validated = v.validate(
    json_object=request_data,
    expected=expected,
    optional=optional
)
```
before importing JVal

# data schema
a data schema is made up of expected (describing each parameter the JSON object must have) 
& optional (describing parameters that may or may not be in JSON object) 

### keys
are python dicts which contain info about parameters of a JSON object.
```
required_params:
    param_name: name of parameter
    param_type: type of parameter

optional_params:
    possible_values: values a parameter can be
    expected: nested expected parameters
    conditional_keys: parameters whose names and values depend on another parameter
```

#### expected keys 
is a list of keys (which are python dict objects defined by the parameters above) describing the required parameters of a JSON object
```
# simple key w/ to limit values of a parameter
simple_key_one =
    {
        "param_name": "source_type",
        "param_type": str,
        "possible_values": ["local", "azure_storage"]
    }
# simple key to check type
simple_key_two =
    {
        "param_name": "source_type",
        "param_type": str
    }
# nested key to validate nested JSON
nested_key =
    {
        "param_name": "store_info",
        "param_type": dict,
        "expected": [
            {"param_name": "host", "param_type": str},
            {"param_name": "dbname", "param_type": str},
            {"param_name": "user", "param_type": str},
            {"param_name": "password", "param_type": str},
            {"param_name": "port", "param_type": int}
        ]
    }
# conditional key
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
                    "expected": [
                        {"param_name": "file_path", "param_type": str}
                    ],
                    # optional keys based on that value
                    "optional": [
                        {"param_name": "dir_path", "param_type": str},
                    ]
                },
                "azure_storage": {
                    "expected": [
                        {"param_name": "connection_string", "param_type": str},
                        {"param_name": "container_name", "param_type": str},
                    ],
                    "optional": [
                        {"param_name": "file_name", "param_type": str}
                    ]
                }
            }
        }
    }
```
#### optional 
list of dicts describing the types & names of each JSON parameter that may or may not be in the JSON object (only checked for types)
```
# simple
simple_key_one =
{
    "param_name": "source_type",
    "param_type": str
}
```
