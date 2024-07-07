from typing import Dict, Any, Set
from models import UsageLimit, UsageLimitType, ValueType, PricingManager
from models.usage_limit_types import NonRenewable, Renewable, ResponseDriven, TimeDriven
from parsers.exceptions import InvalidDefaultValueException, InvalidLinkedFeatureException

class UsageLimitParser:
    @staticmethod
    def parse_map_to_usage_limit(limit_name: str, limit_map: Dict[str, Any], pricing_manager: 'PricingManager') -> 'UsageLimit':
        feature_keys = set(pricing_manager.features.keys())

        try:
            usage_limit_type = UsageLimitType(limit_map["type"])
            if usage_limit_type == UsageLimitType.NON_RENEWABLE:
                return UsageLimitParser.parse_map_to_non_renewable(limit_name, limit_map, feature_keys)
            elif usage_limit_type == UsageLimitType.RENEWABLE:
                return UsageLimitParser.parse_map_to_renewable(limit_name, limit_map, feature_keys)
            elif usage_limit_type == UsageLimitType.RESPONSE_DRIVEN:
                return UsageLimitParser.parse_map_to_response_driven(limit_name, limit_map, feature_keys)
            elif usage_limit_type == UsageLimitType.TIME_DRIVEN:
                return UsageLimitParser.parse_map_to_time_driven(limit_name, limit_map, feature_keys)
            else:
                return None
        except ValueError:
            raise ValueError(f"The usage limit {limit_name} does not have a supported type. Current type value: {limit_map['type']}")

    @staticmethod
    def parse_map_to_non_renewable(limit_name: str, limit_map: Dict[str, Any], feature_keys: Set[str]) -> 'NonRenewable':
        non_renewable = NonRenewable()
        non_renewable.name = limit_name
        UsageLimitParser.set_common_fields(non_renewable, limit_name, limit_map, feature_keys)
        return non_renewable

    @staticmethod
    def parse_map_to_renewable(limit_name: str, limit_map: Dict[str, Any], feature_keys: Set[str]) -> 'Renewable':
        renewable = Renewable()
        renewable.name = limit_name
        UsageLimitParser.set_common_fields(renewable, limit_name, limit_map, feature_keys)
        return renewable

    @staticmethod
    def parse_map_to_response_driven(limit_name: str, limit_map: Dict[str, Any], feature_keys: Set[str]) -> 'ResponseDriven':
        response_driven = ResponseDriven()
        response_driven.name = limit_name
        UsageLimitParser.set_common_fields(response_driven, limit_name, limit_map, feature_keys)
        return response_driven

    @staticmethod
    def parse_map_to_time_driven(limit_name: str, limit_map: Dict[str, Any], feature_keys: Set[str]) -> 'TimeDriven':
        time_driven = TimeDriven()
        time_driven.name = limit_name
        UsageLimitParser.set_common_fields(time_driven, limit_name, limit_map, feature_keys)
        return time_driven

    @staticmethod
    def set_common_fields(limit: 'UsageLimit', limit_name: str, map: Dict[str, Any], feature_keys: Set[str]):
        limit.description = map.get("description")
        limit.value_type = ValueType(map["valueType"])

        try:
            if limit.value_type == ValueType.NUMERIC:
                limit.default_value = map["defaultValue"]
                if not isinstance(limit.default_value, (int, float)):
                    raise InvalidDefaultValueException(
                        f"The usageLimit {limit_name} does not have a valid defaultValue. Current valueType: {limit.value_type}; Current defaultValue: {map['defaultValue']}")
            elif limit.value_type == ValueType.BOOLEAN:
                limit.default_value = bool(map["defaultValue"])
            elif limit.value_type == ValueType.TEXT:
                limit.default_value = str(map["defaultValue"])

            if limit.default_value is None:
                raise InvalidDefaultValueException(
                    f"The usageLimit {limit_name} does not have a valid defaultValue. The actual value is null")
        except KeyError as e:
            raise InvalidDefaultValueException(f"Missing required field in usageLimit {limit_name}: {str(e)}")

        limit.unit = map.get("unit")
        linked_features = map.get("linkedFeatures", [])

        for linked_feature in linked_features:
            if linked_feature not in feature_keys:
                raise InvalidLinkedFeatureException(
                    f"The usageLimit {limit_name} is linked to a nonexistent feature. Current linkedFeature: {linked_feature}")

        limit.linked_features = linked_features
