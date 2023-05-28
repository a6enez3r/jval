"""
Python package to validate JSON data against a schema.

A schema is a Python list containing dictionaries that describe each parameter/key in the JSON
object, both expected and optional.

A schema can have a list of expected (must be in the JSON object) and optional keys (which may
or may not be in the JSON object being validated).

A key is a Python dictionary that can be simple or nested and contains information about a
parameter in the JSON object.

Expected keys: A list of keys, which are Python dict objects describing the required parameters
of a JSON object.

They can be simple, nested, or conditional.

    - Simple:
        simple_key = {
            "param_name": "param_one",
            "param_type": str,
            "possible_values": ["val_one", "val_two"]
        }
        simple_key = {
            "param_name": "source_type",
            "param_type": str
        }

    - Nested:
        nested_key = {
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

    - Conditional:
        conditional_key = {
            "param_name": "source_info",
            "param_type": dict,
            "conditional": {
                "depends_on": "source_type",
                "dependence_info": {
                    "local": {
                        "expected": [
                            {"param_name": "file_path", "param_type": str}
                        ],
                        "optional": [
                            {"param_name": "dir_path", "param_type": str},
                        ]
                    },
                    "azure_storage": {
                        "expected": [
                            {"param_name": "connection_string", "param_type": str},
                            {"param_name": "container_name", "param_type": str}
                        ],
                        "optional": [
                            {"param_name": "file_name", "param_type": str}
                        ]
                    }
                }
            }
        }

Optional keys: A list of dicts describing the types and names of each JSON parameter that may
or may not be in the JSON object. They are only checked for types.

    - Optional:
        optional_key = {
            "param_name": "source_type",
            "param_type": str
        }

Methods:

    - validate: Validate a JSON object against a schema.
    - fvalidate: Validate a JSON file against a schema.
"""

import json
import logging
import os
from logging.config import dictConfig
from typing import Any, Dict, List, Optional

from jval import _version
from jval.common import LOGGING_DICT

__version__ = _version.get_versions()["version"]

dictConfig(LOGGING_DICT)
logger = logging.getLogger(__name__)


class JVal:
    """
    JSON validator class for checking if a given JSON object or file matches a schema.
    """

    def __init__(self):
        """
        Instantiate the JSON validator.
        """

    def _validate_expected(
        self, jobj: Dict[str, Any], expected: Dict[str, Any]
    ) -> bool:
        """
        Recursively validate whether a JSON object satisfies the expected schema.

        Args
        -----
            - jobj (Dict[str, Any]): JSON object to validate.
            - expected (Dict[str, Any]): A list of keys that are Python dict objects describing
                                         the required parameters of a JSON object.

        Returns
        -------
            - bool: True if the JSON object is valid according to the schema, False otherwise.
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

    def _validate_optional(
        self, jobj: Dict[str, Any], optional: Dict[str, Any]
    ) -> bool:
        """
        Recursively validate whether a JSON object satisfies the optional schema.

        Args
        ----
            - jobj (Dict[str, Any]): JSON object to validate.
            - optional (Dict[str, Any]): A list of dicts describing the types & names of each
                                         JSON parameter that may or may not be in the JSON
                                         object.

        Returns
        -------
            - bool: True if the JSON object is valid according to the optional schema, False
                    otherwise.
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

    def _contains_invalid(self, jobj: Dict[str, Any], valid: List[str]) -> bool:
        """
        Check if all the keys in a JSON object are valid keys.

        Valid keys are comprised of expected + optional.

        Args
        ----
            - jobj (Dict[str, Any]): JSON object being validated.
            - valid (List[str]): Name of allowed parameters.

        Returns
        -------
            - bool: List of invalid parameter names found in the JSON object.
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

    def _build_valid(
        self,
        expected: Optional[List[Dict[str, Any]]] = None,
        optional: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Build a valid list of keys from expected and optional keys.

        Args
        ----
            - expected (Optional[List[Dict[str, Any]]]): A list of keys which are python dict
                                                         objects describing the required
                                                         parameters of a JSON object
            - optional (Optional[List[Dict[str, Any]]]): A list of dicts describing the types
                                                         & names of each JSON parameter that
                                                         may or may not be in the JSON object

        Returns
        -------
            - bool: List of valid keys (combination of expected and optional keys).
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

    def validate(
        self,
        jobj: Dict[str, Any],
        expected: Optional[List[Dict[str, Any]]] = None,
        optional: Optional[List[Dict[str, Any]]] = None,
    ) -> bool:
        """
        Validate a JSON object against a schema.

        Parameters:
            - jobj (Dict[str, Any]): JSON object to validate.
            - expected (Optional[List[Dict[str, Any]]]): A list of keys which are python dict
                                                         objects describing the required
                                                         parameters of a JSON object
            - optional (Optional[List[Dict[str, Any]]]): A list of dicts describing the types
                                                         & names of each JSON parameter that
                                                         may or may not be in the JSON object

        Returns:
            - bool: True if the JSON object satisfies the schema, False otherwise.
        """
        # get list of valid param names
        valid = self._build_valid(expected=expected, optional=optional)
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

    def fvalidate(
        self,
        jpath: str,
        expected: Optional[List[Dict[str, Any]]] = None,
        optional: Optional[List[Dict[str, Any]]] = None,
    ) -> bool:
        """
        Validate a JSON file against a schema.

        Args
        ----
            - jpath: Absolute path to the JSON file.
            - expected (Optional[List[Dict[str, Any]]]): A list of keys which are python dict
                                                         objects describing the required
                                                         parameters of a JSON object
            - optional (Optional[List[Dict[str, Any]]]): A list of dicts describing the types
                                                         & names of each JSON parameter that
                                                         may or may not be in the JSON object

        Returns
        -------
            - bool: True if the JSON file satisfies the schema, False otherwise.
        """
        with open(jpath, "rb") as jfile:
            jobj = json.loads(jfile)
            return self.validate(jobj, expected=expected, optional=optional)
