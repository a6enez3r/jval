# validateJSON ![build](https://github.com/abmamo/validateJSON/workflows/build/badge.svg?branch=main)
package to validate JSON data against a schema

the data schema consists of:
- expected_keys: list of dicts describing the types & names
                 of each JSON parameter that MUST be in the
                 JSON object
- conditional_keys: list of dicts describing the type, name
                    and dependence info of a set of each JSON
                    parameter that MUST be in the JSON
                    object
- optional_keys: list of dicts describing the types & names
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
3. define data schema (sample data schema below)
```
# sample JSON data
request_data = {
    "type": "local",
    "store_info":
        {
            "host": "localhost",
            "dbname": "postgres",
            "user": "postgres",
            "password": "testpassword",
            "port": 5432,
            "layer": {
                "layer_test": 123
            }
        },
    "file_path": "value"
}
# expected parameters
expected = [
    # source type
    {
        "param_name": "type",
        "param_type": str,
        "possible_values": ["local", "azure_storage"]},
    # db connection info
    {
        "param_name": "store_info",
        "param_type": dict,
        "expected_keys": [
            {"param_name": "host", "param_type": str},
            {"param_name": "dbname", "param_type": str},
            {"param_name": "user", "param_type": str},
            {"param_name": "password", "param_type": str},
            {"param_name": "port", "param_type": int},
            {
                "param_name": "layer",
                "param_type": dict,
                "expected_keys":
                    [
                        {"param_name": "layer_test", "param_type": int}
                    ]
            }
        ]
    },
]
# conditional parameters
conditional = [
    # source connection info
    {
        "depends_on": "type",
        "depdendence_info": {
            "local": [
                {"param_name": "file_path", "param_type": str}
            ],
            "azure_storage": [
                {"param_name": "connection_string", "param_type": str}
            ]
        }
    }
]
```
4. run validator
```
from validateJSON import JSONValidator
# init validator
v = JSONValidator()
# pass test data
validated = v.validate(
    json_object=request_data,
    expected_keys=expected,
    conditional_keys=conditional
)
```
