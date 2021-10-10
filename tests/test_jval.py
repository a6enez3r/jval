"""
    tests for jval JSON data validator
"""
import pytest

from jval import JVal


@pytest.fixture
def test_data():
    """valid JSON test data"""
    return {
        "source_type": "azure_storage",
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_string": "ha",
        },
        "store_type": "pg",
        "store_info": {
            "host": "localhost",
            "dbname": "postgres",
            "user": "abmamo",
            "password": "testpassword",
            "port": 5432,
        },
    }


@pytest.fixture
def missing_expected():
    """invalid JSON data missing expected keys"""
    return {
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_string": "",
        },
        "store_type": "pg",
        "store_info": {
            "host": "localhost",
            "dbname": "postgres",
            "user": "abmamo",
            "password": "testpassword",
            "port": 5432,
        },
    }


@pytest.fixture
def incorrect_type():
    """invalid JSON data with an incorrect parameter type"""
    return {
        "source_type": "azure_storage",
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_string": 1,
        },
        "store_type": "pg",
        "store_info": {
            "host": "localhost",
            "dbname": "postgres",
            "user": "abmamo",
            "password": "testpassword",
            "port": 5432,
        },
    }


@pytest.fixture
def incorrect_possible():
    """invalid JSON data with an invalid value for a property"""
    return {
        "source_type": "gcp_storage",
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_string": "",
        },
        "store_type": "pg",
        "store_info": {
            "host": "localhost",
            "dbname": "postgres",
            "user": "abmamo",
            "password": "testpassword",
            "port": 5432,
        },
    }


@pytest.fixture
def incorrect_nested():
    """invalid JSON data with an invalid nested value for a property"""
    return {
        "source_type": "azure_storage",
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_stringg": "",
        },
        "store_type": "pg",
        "store_info": {
            "host": "localhost",
            "dbname": "postgres",
            "user": "abmamo",
            "password": "testpassword",
            "port": 5432,
        },
    }


@pytest.fixture
def incorrect_optional_type():
    """invalid JSON data with an invalid type for an optional property"""
    return {
        "source_type": 1,
        "source_info": {
            "file_name": "<file path here>",
            "container_name": "<some container name here>",
            "connection_string": "",
        },
        "store_type": "pg",
        "store_info": {
            "host": "localhost",
            "dbname": "postgres",
            "user": "abmamo",
            "password": "testpassword",
            "port": 5432,
        },
    }


@pytest.fixture
def test_schema():
    """test schema"""
    return [
        # simple key
        {
            "param_name": "store_type",
            "param_type": str,
            "possible_values": ["pg", "mysql"],
        },
        # nested key
        {
            "param_name": "store_info",
            "param_type": dict,
            "expected": [
                {"param_name": "host", "param_type": str},
                {"param_name": "dbname", "param_type": str},
                {"param_name": "user", "param_type": str},
                {"param_name": "password", "param_type": str},
                {"param_name": "port", "param_type": int},
            ],
        },
        # possible values
        {
            "param_name": "source_type",
            "param_type": str,
            "possible_values": ["local", "azure_storage"],
        },
        # conditional key
        {
            "param_name": "source_info",
            "param_type": dict,
            "conditional": {
                "depends_on": "source_type",
                "dependence_info": {
                    "local": {
                        "expected": [{"param_name": "file_path", "param_type": str}],
                        "optional": [
                            {"param_name": "dir_path", "param_type": str},
                        ],
                    },
                    "azure_storage": {
                        "expected": [
                            {"param_name": "connection_string", "param_type": str},
                            {"param_name": "container_name", "param_type": str},
                        ],
                        "optional": [{"param_name": "file_name", "param_type": str}],
                    },
                },
            },
        },
    ]


def test_validator_valid_expected(
    test_data, test_schema  # pylint: disable=redefined-outer-name
):
    """test validator expected validation"""
    validated = JVal().validate(
        jobj=test_data,
        expected=test_schema,
    )
    assert validated is True


def test_validator_valid_optional(
    test_data, test_schema  # pylint: disable=redefined-outer-name
):
    """test validator optional validation"""
    validated = JVal().validate(
        jobj=test_data,
        optional=test_schema,
    )
    assert validated is True


def test_validator_missing_expected(
    missing_expected, test_schema  # pylint: disable=redefined-outer-name
):
    """test validator missing expected keys validation"""
    validated = JVal().validate(
        jobj=missing_expected,
        expected=test_schema,
    )
    assert validated is False


def test_validator_incorrect_type(
    incorrect_type, test_schema  # pylint: disable=redefined-outer-name
):
    """test validator keys with incorrect types validation"""
    validated = JVal().validate(
        jobj=incorrect_type,
        expected=test_schema,
    )
    assert validated is False


def test_validator_incorrect_possible(
    incorrect_possible, test_schema  # pylint: disable=redefined-outer-name
):
    """test validator keys with incorrect possible value validation"""
    validated = JVal().validate(
        jobj=incorrect_possible,
        expected=test_schema,
    )
    assert validated is False


def test_validator_incorrect_nested_expected(
    incorrect_nested, test_schema  # pylint: disable=redefined-outer-name
):
    """test validator keys with incorrect nested expected values validation"""
    validated = JVal().validate(
        jobj=incorrect_nested,
        expected=test_schema,
    )
    assert validated is False


def test_validator_incorrect_optional_type(
    incorrect_optional_type, test_schema
):  # pylint: disable=redefined-outer-name
    """test validator keys with incorrect nested expected values validation"""
    validated = JVal().validate(
        jobj=incorrect_optional_type,
        optional=test_schema,
    )
    assert validated is False
