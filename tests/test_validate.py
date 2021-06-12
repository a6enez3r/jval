# testing
import pytest
# validator & its logger
from validate_json import JSONValidator

@pytest.fixture(scope="module")
def test_request_data():
    # test data
    test_request_data = {
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
    return test_request_data

@pytest.fixture(scope="module")
def test_request_data_missing_expected():
    # test data
    test_request_data_missing_expected = {
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
    return test_request_data_missing_expected


@pytest.fixture(scope="module")
def test_request_data_incorrect_type():
    # test data
    test_request_data_incorrect_type = {
        "source_type": "azure_storage",
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_string": 1
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
    return test_request_data_incorrect_type


@pytest.fixture(scope="module")
def test_request_data_incorrect_possible():
    # test data
    test_request_data_incorrect_possible = {
        "source_type": "gcp_storage",
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
    return test_request_data_incorrect_possible


@pytest.fixture(scope="module")
def test_request_data_incorrect_nested_expected():
    # test data
    test_request_data_incorrect_nested_expected = {
        "source_type": "azure_storage",
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_stringg": ""
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
    return test_request_data_incorrect_nested_expected

@pytest.fixture(scope="module")
def test_request_data_incorrect_optional_type():
    # test data
    test_request_data_incorrect_optional_type = {
        "source_type": 1,
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
    return test_request_data_incorrect_optional_type

@pytest.fixture(scope="module")
def test_request_schema():
    # test data schema
    test_request_schema = [
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
    return test_request_schema


def test_validator_valid_expected_and_optional(test_request_data, test_request_schema):
    # init validator
    v = JSONValidator()
    # pass test data
    validated = v.validate(
        json_object=test_request_data,
        expected_keys=test_request_schema,
    )
    # assert validated is true
    assert validated == True


def test_validator_valid_optional(test_request_data, test_request_schema):
    # init validator
    v = JSONValidator()
    # pass test data
    validated = v.validate(
        json_object=test_request_data,
        optional_keys=test_request_schema,
    )
    # assert validated is true
    assert validated == True


def test_validator_missing_expected(test_request_data_missing_expected, test_request_schema):
    # init validator
    v = JSONValidator()
    # pass test data
    validated = v.validate(
        json_object=test_request_data_missing_expected,
        expected_keys=test_request_schema,
    )
    # assert validated is true
    assert validated == False

def test_validator_incorrect_type(test_request_data_incorrect_type, test_request_schema):
    # init validator
    v = JSONValidator()
    # pass test data
    validated = v.validate(
        json_object=test_request_data_incorrect_type,
        expected_keys=test_request_schema,
    )
    # assert validated is true
    assert validated == False

def test_validator_incorrect_possible(test_request_data_incorrect_possible, test_request_schema):
    # init validator
    v = JSONValidator()
    # pass test data
    validated = v.validate(
        json_object=test_request_data_incorrect_possible,
        expected_keys=test_request_schema,
    )
    # assert validated is true
    assert validated == False

def test_validator_incorrect_nexted_expected(test_request_data_incorrect_nested_expected, test_request_schema):
    # init validator
    v = JSONValidator()
    # pass test data
    validated = v.validate(
        json_object=test_request_data_incorrect_nested_expected,
        expected_keys=test_request_schema,
    )
    # assert validated is true
    assert validated == False

def test_validator_incorrect_optional_type(test_request_data_incorrect_optional_type, test_request_schema):
    # init validator
    v = JSONValidator()
    # pass test data
    validated = v.validate(
        json_object=test_request_data_incorrect_optional_type,
        optional_keys=test_request_schema,
    )
    # assert validated is true
    assert validated == False