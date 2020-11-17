# logging
import logging
# set up logging before importing sub modules
from validateJSON.logs import setup_logging
# configure logging
logger = setup_logging(logging.getLogger(__name__))


class JSONValidator:
    """
        validate JSON data against a data schema. a data schema is a
        python list containing dictionaries describing each parameter
        in the JSON object. a data schema can have a list of
        expected keys (must be in JSON object) and a list of
        optional keys (may or may not be in JSON object)

        expected keys: is a list of keys which are python dict objects
                       describing the required parameters of a JSON object.

                       keys: are python dicts which can be simple or nested
                             & contain information about dependence b/n
                             parameters of a JSON object

                             required_params:
                                "param_name": name of parameter
                                "param_type": type of parameter
                             optional_params:
                                "possible_values": values a parameter can be
                                "expected_keys": nested JSON object
                                "conditional_keys": parameters whose names and
                                                    values depend on another parameter


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

        - optional_keys: list of dicts describing the types & names
                         of each JSON parameter that may or may not
                         be in the JSON object (only checked for types)

                         # simple
                         simple_key_one =
                            {
                                "param_name": "source_type",
                                "param_type": str
                            }
    """
    def validate_expected(self, json_object, expected_keys):
        """
            recursively validate JSON object satisfies expected schema

            params:
                - json_object: JSON object to validate
                - expected_keys: is a list of keys which are python dict objects
                                 describing the required parameters of a JSON object
            returns
                - is_valid: True or False
        """
        # validate all expected parameters are in JSON object
        contains_params = [
            # check parameter name in json object
            parameter in json_object for parameter in
            # for each parameter in expected_keys / data schema
            [expected_key["param_name"] for expected_key in expected_keys]
        ]
        # if there are any missing expected parameters
        if not all(contains_params):
            # get missing parameter names
            missing_keys = [
                # get param name
                expected_key_name["param_name"]
                for expected_key_name, exists in
                zip(expected_keys, contains_params)
                # if it doesn't exist in json object
                if not exists]
            # log
            logger.error("missing expected: %s" % missing_keys)
            # return False (invalid JSON object)
            return False
        # if there are no missing expected parameters
        else:
            # validate expected parameters' types
            correct_types = [
                # check if type matches specified in schema
                isinstance(
                    # get value from json object
                    json_object[expected_key["param_name"]],
                    # get expected type from schema
                    expected_key["param_type"]
                )
                # for each parameter in expected_keys / data schema
                for expected_key in expected_keys
            ]
            # if there are any expected parameters with an incorrect type
            if not all(correct_types):
                # get parameter names with invalid types
                incorrect_type_keys = [
                    # get param name
                    expected_key_name["param_name"]
                    for expected_key_name, correct_type in
                    zip(expected_keys, correct_types)
                    # if it doesn't have correct type
                    if not correct_type
                ]
                # log
                logger.error("incorrect type for: %s" % incorrect_type_keys)
                # return False (invalid JSON object)
                return False
            # if there are no parameters missing or incorrect types
            else:
                # for each expected parameter
                for expected_key in expected_keys:
                    # possible values parameter can be
                    if "possible_values" in expected_key:
                        # if val in JSON is not one of possible vals
                        if json_object[expected_key["param_name"]] not in expected_key["possible_values"]:
                            # log
                            logger.error("incorrect possible value: %s, for param: %s" % (
                                    json_object[expected_key["param_name"]],
                                    expected_key["param_name"])
                                )
                            # return False (invalid JSON object)
                            return False
                    # nested parameters
                    if expected_key["param_type"] == dict:
                        # if expected keys / schema specified in schema
                        # for nested dict
                        if "expected_keys" in expected_key:
                            # recursively run above validation logic on nested
                            # JSON object
                            if not self.validate_expected(
                                # get nested value of dict from JSON object
                                json_object[expected_key["param_name"]],
                                # get nested expected keys from schema
                                expected_key["expected_keys"]
                            ):
                                # return False (invalid JSON object)
                                return False
                        # parameters that depend on value of parameter
                        # in JSON object
                        if "conditional_keys" in expected_key:
                            # get the value the conditional keys depend on from JSON object
                            depends_on_val = json_object[expected_key["conditional_keys"]["depends_on"]]
                            # get depdendence info (i.e. based on the above value
                            # get what the expected / optional keys are)
                            nested_optional_keys = expected_key["conditional_keys"]["dependence_info"][depends_on_val]["optional_keys"]
                            nested_expected_keys = expected_key["conditional_keys"]["dependence_info"][depends_on_val]["expected_keys"]
                            # recursively run optional & expected validation
                            return self.validate(
                                json_object[expected_key["param_name"]],
                                nested_expected_keys,
                                nested_optional_keys
                            )
                # return True (valid JSON object)
                return True

    def validate_optional(self, json_object, optional_keys):
        """
            recursively validate JSON object satisfies optional schema

            params:
                - json_object: JSON object being validated
                - optional_keys: list of dicts describing the types & names
                                 of each JSON parameter that may or may not
                                 be in the JSON object
            returns
                - is_valid: True or False
        """
        # for all optional keys specified
        for optional_key in optional_keys:
            # if they are in the json object
            if optional_key["param_name"] in json_object:
                # validate type
                correct_type = isinstance(
                    # get value from JSON object
                    json_object[optional_key["param_name"]],
                    # get type from schema
                    optional_key["param_type"])
                # if not correct type
                if not correct_type:
                    # log
                    logger.error("invalid optional type: %s for param: %s" % (correct_type, optional_key))
                    # return False (invalid JSON object)
                    return False
                # if optional parameter is a nested JSON
                if optional_key["param_type"] == dict:
                    # if it has optional parameters specified
                    if "optional_keys" in optional_key:
                        # run validation recursively
                        return self.validate_optional(
                            # pass nested JSON object
                            json_object[optional_key["param_name"]],
                            # pass nested JSON object schema
                            optional_key["optional_keys"]
                        )
        return True

    def validate(self, json_object, expected_keys, optional_keys=None):
        """
            validate JSON object against a schema

            a schema = expected_keys + optional_keys
                - expected_keys :- is a list of keys which are python dict objects
                                   describing the required parameters of a JSON object

                - optiona_keys :- list of dicts describing the types & names
                                  of each JSON parameter that may or may not
                                  be in the JSON object
        """
        # create list of expected + optional keys to check if
        # any unnecessary parameters passed in JSON object
        if optional_keys is not None:
            # valid_keys = expected_keys + optional_keys
            valid_keys = [expected_key["param_name"] for expected_key in expected_keys] + [optional_key["param_name"] for optional_key in optional_keys]
        # no optional parameters specified
        else:
            # valid_keys = expected_keys
            valid_keys = [expected_key["param_name"] for expected_key in expected_keys]
        # check if any parameter present in JSON object is not in valid_keys (i.e. check
        # it is allowed)
        contains_valid = [
            # for each param in json object
            parameter in valid_keys for parameter in json_object
        ]
        # if any invalid parameter detected
        if not all(contains_valid):
            # get names of invalid parameters
            invalid_keys = [
                # name of key
                invalid_key for
                invalid_key, is_valid in
                zip(list(json_object.keys()), contains_valid)
                # if it is not valid / not in expected_keys or optional_keys
                if not is_valid
            ]
            # log
            logger.error("invalid: %s" % invalid_keys)
            # return False (invalid JSON object)
            return False
        # run expected validation
        if self.validate_expected(json_object, expected_keys):
            # if optional parameters are specified
            if optional_keys is not None:
                # run optional validation
                if self.validate_optional(json_object, optional_keys):
                    # return success
                    return True
                else:
                    # return failure (optional failed)
                    return False
            # no optional keys specified return
            else:
                return True
        # validation failure (expected failed)
        else:
            return False
