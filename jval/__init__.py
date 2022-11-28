"""
    ***

    python package to validate JSON data against a schema.

    a **schema** is a python list containing dictionaries
    describing each parameter / key in the JSON object (both
    expected and optional)

    ***

    a **schema** can have a list of *expected* (must be in the
    JSON object) and *optional* keys (which may or may not be
    in the JSON object being validated)

    a **key** is a python dictionary which can be simple or nested
    and _contains information about a parameter in the JSON object

    ***

    **expected keys**: is a list of keys, which are python dict objects
                        describing the required parameters of a JSON object.
                        can be either `simple`, `nested`, or `conditional`

        # simple
        simple_key =
        {
            "param_name": "param_one",
            "param_type": str,
            "possible_values": ["val_one", "val_two"]
        }
        simple_key =
        {
            "param_name": "source_type",
            "param_type": str
        }
        # nested
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
        # conditional
        conditional_key =
        {
            "param_name": "source_info",
            "param_type": dict,
            "conditional": {
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
                            {
                                "param_name": "connection_string",
                                "param_type": str
                            },
                            {
                                "param_name": "container_name",
                                "param_type": str
                            },
                        ],
                        "optional": [
                            {"param_name": "file_name", "param_type": str}
                        ]
                    }
                }
            }
        }

    ***

    **optional keys** : list of dicts describing the types & names
                        of each JSON parameter that may or may not
                        be in the JSON object (are only checked for types)
            # optional
            optional_key =
            {
                "param_name": "source_type",
                "param_type": str
            }
    ***

    **methods**

    ***

    **validate**: validate a JSON object against a schema

    **fvalidate**: validate a JSON file against a schema

    ***
"""
import os
import json
import logging
from logging.config import dictConfig

from jval import _version
from jval.common import LOGGING_DICT

__version__ = _version.get_versions()["version"]


dictConfig(LOGGING_DICT)
logger = logging.getLogger(__name__)


class JVal:
    """
    check a given JSON object or file matches a schema
    """

    def __init__(self):
        """instantitate json validator"""

    def _validate_expected(self, jobj, expected):
        """
        recursively validate JSON object satisfies expected schema

        params:
            - jobj: JSON object to validate
            - expected: is a list of keys which are python dict objects
                             describing the required parameters of a JSON object
        returns
            - is_valid: True or False
        """
        _contains_params = [
            parameter in jobj
            for parameter in [expected_key["param_name"] for expected_key in expected]
        ]
        # validate missing
        if not all(_contains_params):
            # get missing parameter names
            missing = [
                # get param name
                expected_key_name["param_name"]
                for expected_key_name, exists in zip(expected, _contains_params)
                # if it doesn't exist in json object
                if not exists
            ]
            logger.error("missing expected: %s", missing)
            return False
        # validate types
        correct_types = [
            # check if type matches specified in schema
            isinstance(
                jobj[expected_key["param_name"]],
                expected_key["param_type"],
            )
            for expected_key in expected
        ]
        # if there are any invalid types
        if not all(correct_types):
            # get parameter names with invalid types
            incorrect_type = [
                expected_key_name["param_name"]
                for expected_key_name, correct_type in zip(expected, correct_types)
                if not correct_type
            ]
            # log & return
            logger.error("incorrect type for: %s", incorrect_type)
            return False

        for expected_key in expected:
            # validate possible values
            if "possible_values" in expected_key:
                if (
                    jobj[expected_key["param_name"]]
                    not in expected_key["possible_values"]
                ):
                    # log & return
                    logger.error(
                        "incorrect possible value: %s, for param: %s",
                        jobj[expected_key["param_name"]],
                        expected_key["param_name"],
                    )
                    return False
            # validate nested
            if expected_key["param_type"] == dict:
                # validate nested expected
                if "expected" in expected_key:
                    if not self._validate_expected(
                        jobj[expected_key["param_name"]],
                        expected_key["expected"],
                    ):
                        return False
                # validate conditional expected
                if "conditional" in expected_key:
                    # get the value the conditional keys depend on from JSON object
                    depends_on_val = jobj[expected_key["conditional"]["depends_on"]]
                    # get depdendence info (i.e. based on the above value
                    # get what the expected / optional keys are)
                    nested_optional = expected_key["conditional"]["dependence_info"][
                        depends_on_val
                    ]["optional"]
                    nested_expected = expected_key["conditional"]["dependence_info"][
                        depends_on_val
                    ]["expected"]
                    # recursively run optional & expected validation
                    return self.validate(
                        jobj[expected_key["param_name"]],
                        nested_expected,
                        nested_optional,
                    )
        return True

    def _validate_optional(self, jobj, optional):
        """
        recursively validate JSON object satisfies optional schema

        params:
            - jobj: JSON object being validated
            - optional: list of dicts describing the types & names
                             of each JSON parameter that may or may not
                             be in the JSON object
        returns
            - is_valid: True or False
        """
        for optional_key in optional:
            # validate all optional keys in json object
            if optional_key["param_name"] in jobj:
                # validate types
                correct_type = isinstance(
                    jobj[optional_key["param_name"]],
                    optional_key["param_type"],
                )
                if not correct_type:
                    # log & return
                    logger.error(
                        "invalid optional type: %s for param: %s",
                        correct_type,
                        optional_key,
                    )
                    return False
                # validate nested optional
                if optional_key["param_type"] == dict:
                    # if it has optional parameters specified
                    # run validation recursively
                    if "optional" in optional_key:
                        return self._validate_optional(
                            jobj[optional_key["param_name"]],
                            optional_key["optional"],
                        )
        return True

    def _contains_invalid(self, jobj, valid):
        """
        check if all the keys in a JSON object are valid keys

        valid keys are comprised of expected + optional

        params:
            - jobj: JSON object being validated
            - valid: name of allowed parameters
        returns:
            - bool True or False (if it _contains invalid param name)
        """
        # check if any parameter present in JSON object is not in valid / matches
        # the schema
        only_valid = [parameter in valid for parameter in jobj]
        # if any invalid parameter detected
        if not all(only_valid):
            # get names of invalid parameters
            invalid = [
                invalid_key
                for invalid_key, is_valid in zip(list(jobj.keys()), only_valid)
                if not is_valid
            ]
            return invalid
        return []

    def _build_valid(self, expected=None, optional=None):
        """
        build valid list of keys from expected + optional keys

        params:
            - expected :- is a list of keys which are python dict objects
                               describing the required parameters of a JSON object

            - optional :- list of dicts describing the types & names
                              of each JSON parameter that may or may not
                              be in the JSON object
        """

        if expected is not None:
            if optional is not None:
                # if expected keys specified + optional keys specified
                # valid keys = expected keys + optional keys
                valid = [expected_key["param_name"] for expected_key in expected] + [
                    optional_key["param_name"] for optional_key in optional
                ]
            else:
                # if expected keys specified + no optional keys specified
                # valid = expected
                valid = [expected_key["param_name"] for expected_key in expected]
        else:
            if optional is None:
                # no optional or expected keys specified
                # valid keys = empty list
                valid = []
            else:
                # no expected key but optional keys specified
                # valid keys = optional keys
                valid = [optional_key["param_name"] for optional_key in optional]
        return valid

    def validate(self, jobj, expected=None, optional=None):
        """
        validate JSON object against a schema

        ***

        **parameters**

        ***

        *expected*: list of keys which are python dict objects
                    describing the required parameters of a JSON object

        *optional*: list of dicts describing the types & names
                    of each JSON parameter that may or may not
                    be in the JSON object

        *schema*: `expected` + `optional`
        ***
        """
        print(expected)
        # get list of valid param names
        valid = self._build_valid(expected=expected, optional=optional)
        print(valid)
        # if no param names -> no expected or optional found
        if len(valid) == 0:
            # log & return
            logger.error("no optional or expected specified")
            return False
        # check if any parameter present in JSON object is not in valid (i.e. check
        # it is allowed)
        invalid = self._contains_invalid(jobj=jobj, valid=valid)
        if invalid:
            return False
        # run validation
        if expected is not None:
            if optional is not None:
                return self._validate_optional(
                    jobj, optional
                ) and self._validate_expected(jobj, expected)
            return self._validate_expected(jobj, expected)
        if optional is not None:
            return self._validate_optional(jobj, optional)
        return True

    def fvalidate(self, jpath, expected=None, optional=None):
        """
        ***

        validate JSON file against a schema

        ***

        **parameters**

        ***

        *jpath*: absolute path to JSON file

        *expected*: list of keys which are python dict objects
                    describing the required parameters of a JSON object

        *optional*: list of dicts describing the types & names
                    of each JSON parameter that may or may not
                    be in the JSON object

        *schema*: `expected` + `optional`
        ***
        """
        with open(jpath, "rb") as jfile:
            jobj = json.loads(jfile)
            return self.validate(jobj, expected=expected, optional=optional)
