# validator & its logger
from validateJSON import JSONValidator


def test_validator_invalid():
    # test data
    request_data_one = {
        "source_type": "local",
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_string": ""
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
    request_data_two = request_data = {
        "source_type": "azure_storage",
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
    
    # test data schema
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
    # init validator
    v = JSONValidator()
    # pass test data
    validated_one = v.validate(
        json_object=request_data_one,
        expected_keys=expected,
    )
    validated_two = v.validate(
        json_object=request_data_two,
        expected_keys=expected,
    )
    # assert validated is true
    assert validated_one == False
    assert validated_two == False

def test_validator_valid():
    # test data
    request_data_one = {
        "source_type": "azure_storage",
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_string": ""
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
    request_data_two = request_data = {
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
    
    # test data schema
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
    # init validator
    v = JSONValidator()
    # pass test data
    validated_one = v.validate(
        json_object=request_data_one,
        expected_keys=expected,
    )
    validated_two = v.validate(
        json_object=request_data_two,
        expected_keys=expected,
    )
    # assert validated is true
    assert validated_one == True
    assert validated_two == True