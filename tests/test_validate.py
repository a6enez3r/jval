# validator & its logger
from validateJSON import JSONValidator


def test_validator_valid():
    # test data
    request_data = {
        "type": "local",
        "store_info":
            {
                "host": "localhost",
                "dbname": "postgres",
                "user": "abmamo",
                "password": "testpassword",
                "port": 5432,
                "layer": {
                    "layer_test": 123
                }
            },
        "file_path": "value"
    }

    # validate parameters
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
    # init validator
    v = JSONValidator()
    # pass test data
    validated = v.validate(
        json_object=request_data,
        expected_keys=expected,
        conditional_keys=conditional
    )
    # assert validated is true
    assert validated == True

def test_validator_valid():
    # test data
    request_data = {
        "type": "local",
        "store_info":
            {
                "host": "localhost",
                "dbname": "postgres",
                "user": "abmamo",
                "password": "testpassword",
                "port": 5432,
                "layer": {
                    "layer_test": 123
                }
            }
    }

    # validate parameters
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
    # init validator
    v = JSONValidator()
    # pass test data
    validated = v.validate(
        json_object=request_data,
        expected_keys=expected,
        conditional_keys=conditional
    )
    # assert validated is true
    assert validated == False
