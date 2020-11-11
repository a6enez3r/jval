# logging
import logging
# set up logging before importing sub modules
from validateJSON.logs import setup_logging
# configure logging
logger = setup_logging(logging.getLogger(__name__))


class JSONValidator:
    """
        validate JSON data using data schema

        the data schema consists of:
        - expected_keys: list of dicts describing the types & names
                         of each JSON parameter that MUST be in the
                         JSON object
        - conditional_keys: list of dicts describing the type, name
                            and dependence info of a set of each JSON
                            parameter that MUST be in the JSON
                            object
        - expected_keys: list of dicts describing the types & names
                         of each JSON parameter that may or may not
                         be in the JSON object
    """
    def validate_expected(self, json_object, expected_keys):
        """
            recursively check a list of parameters are in a
            given JSON object and have the right type

            params:
                - json_object: JSON object being validated
                - expected_keys: list of dicts describing JSON object
            returns
                - True or False
        """
        # validate all expected parameters are in JSON object
        contains_params = [
            parameter in json_object for parameter in
            [expected_key["param_name"] for expected_key in expected_keys]
        ]
        # if there is any missing parameter
        if not all(contains_params):
            # log
            logger.error("missing expected parameter")
            # return False (invalid JSON object)
            return False
        else:
            # validate all expected parameters have correct type
            correct_types = [
                isinstance(
                    # get value from json object
                    json_object[expected_key["param_name"]],
                    # get expected type from schema
                    expected_key["param_type"]
                )
                for expected_key in expected_keys
            ]
            # if there is any incorrect type
            if not all(correct_types):
                # log
                logger.error("incorrect expected parameter type")
                # return False (invalid JSON object)
                return False
            else:
                # for each expected parameter
                for expected_key in expected_keys:
                    # if expected key type is dict
                    if expected_key["param_type"] == dict:
                        # if expected keys specified in schema for nested dict
                        if "expected_keys" in expected_key:
                            # recursively run above logic on any nested
                            # JSON object (i.e. any params of type dict)
                            return self.validate_expected(
                                # get value of dict from JSON object
                                json_object[expected_key["param_name"]],
                                # get expected keys from schema
                                expected_key["expected_keys"]
                            )
                # return True (valid JSON object)
                return True

    def validate_conditional(self, json_object, conditional_keys):
        """
            check if a given JSON object contains a set of keys
            conditionally based on another value in the same JSON
            object

            params:
                - json_object: JSON object being validated
                - conditional_keys: list of dicts describing JSON object
                                    parameter conditional relations
            returns
                - True or False
        """
        # if conditional keys specified
        if conditional_keys is not None:
            # iterate through all conditional keys
            for conditional_key in conditional_keys:
                # get the value/param it depends on from the json object
                independent_value = json_object[conditional_key["depends_on"]]
                # get expected schema for the dependent param
                # based on the value of the independent param
                conditional_expected = conditional_key["depdendence_info"][independent_value]
                # run validation
                return self.validate_expected(
                    # pass json object unchanged
                    json_object=json_object,
                    # pass schema derived based on
                    # independent param
                    expected_keys=conditional_expected
                )

    def validate_optional(self, json_object, optional_keys):
        """
            recursively check the types of a given set of
            parameters if they exist in a given JSON object

            params:
                - json_object: JSON object being validated
                - expected_keys: list of dicts describing JSON object
            returns
                - True or False
        """
        # for all optional keys
        for optional_key in optional_keys:
            # if they are in the json object
            if optional_key["param_name"] in json_object:
                # validate optional types
                correct_type = isinstance(
                    # get value from JSON object
                    json_object[optional_key["param_name"]],
                    # get type from schema
                    optional_key["param_type"])
                # if not correct type
                if not correct_type:
                    # log
                    logger.error("invalid optional parameter type")
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

    def validate(self, json_object, expected_keys, conditional_keys, optional_keys=None):
        """
            check if a given JSON object
            - contains a given set of keys with given types
            - contains conditional parameters whose value & type is
              determined by expected keys
            - contains optional parameters with given types
        """
        # run expected validation
        if self.validate_expected(json_object, expected_keys):
            # run conditional validation
            if self.validate_conditional(json_object, conditional_keys):
                # if optional parameters are specified
                if optional_keys is not None:
                    # run optional validation
                    if self.validate_optional(json_object, optional_keys):
                        # return success
                        return True
                    else:
                        # return failure
                        return False
                # no optional keys specified return
                else:
                    return True
            # validation failed (missing expected parameter or invalid type)
            else:
                return False
        # validation failed (missing expected parameter or invalid type)
        else:
            return False
