from typing import Dict, Any
from models import PricingManager, ValueType, UsageLimit, Feature, Plan
from models.feature_types import PaymentType
from parsers.exceptions import PricingParsingException, FeatureNotFoundException, InvalidDefaultValueException

class PlanParser:
    @staticmethod
    def parse_map_to_plan(plan_name: str, map: Dict[str, Any], pricing_manager: 'PricingManager') -> 'Plan':
        if plan_name is None:
            raise PricingParsingException("A plan name cannot be null")

        plan = Plan()
        plan.name = plan_name
        plan.description = map.get("description")

        if PlanParser.is_valid_price(map.get("monthlyPrice")) and PlanParser.is_valid_price(map.get("annualPrice")):
            if map.get("monthlyPrice") is None and map.get("annualPrice") is None:
                raise PricingParsingException(f"You have to specify, at least, either a monthlyPrice or an annualPrice for the plan {plan_name}")

            plan.monthly_price = map.get("monthlyPrice")
            plan.annual_price = map.get("annualPrice")
        else:
            raise PricingParsingException(f"Either the monthlyPrice or annualPrice of the plan {plan_name} is neither a valid number nor String")

        plan.unit = map.get("unit")
        PlanParser.set_features_to_plan(plan_name, map, pricing_manager, plan)
        PlanParser.set_usage_limits_to_plan(plan_name, map, pricing_manager, plan)

        return plan

    @staticmethod
    def set_features_to_plan(plan_name: str, map: Dict[str, Any], pricing_manager: 'PricingManager', plan: 'Plan'):
        global_features_map = pricing_manager.features
        plan_features_map = map.get("features", {})
        plan_features = {}

        for plan_feature_name, plan_feature_value in plan_features_map.items():
            if plan_feature_name not in global_features_map:
                raise FeatureNotFoundException(f"The feature {plan_feature_name} is not defined in the global features")

            feature = Feature.clone_feature(global_features_map[plan_feature_name])
            feature.value = plan_feature_value

            if feature.value_type == ValueType.NUMERIC:
                if not isinstance(feature.value, (int, float)):
                    raise InvalidDefaultValueException(
                        f"The feature {plan_feature_name} does not have a valid value. Current valueType: {feature.value_type}; Current value in {plan.name}: {plan_feature_value}")
            elif feature.value_type == ValueType.BOOLEAN:
                if not isinstance(feature.value, bool):
                    raise InvalidDefaultValueException(
                        f"The feature {plan_feature_name} does not have a valid value. Current valueType: {feature.value_type}; Current value in {plan.name}: {plan_feature_value}")
            elif feature.value_type == ValueType.TEXT:
                if not isinstance(feature.value, str):
                    raise InvalidDefaultValueException(
                        f"The feature {plan_feature_name} does not have a valid value. Current valueType: {feature.value_type}; Current value in {plan.name}: {plan_feature_value}")

            plan_features[plan_feature_name] = feature

        plan.features = plan_features

    @staticmethod
    def set_usage_limits_to_plan(plan_name: str, map: Dict[str, Any], pricing_manager: 'PricingManager', plan: 'Plan'):
        global_usage_limits_map = pricing_manager.usage_limits
        plan_usage_limits_map = map.get("usageLimits", {})

        for plan_usage_limit_name, plan_usage_limit_value in plan_usage_limits_map.items():
            if plan_usage_limit_name not in global_usage_limits_map:
                raise FeatureNotFoundException(f"The feature {plan_usage_limit_name} is not defined in the global features")

            usage_limit = UsageLimit.clone_usage_limit(global_usage_limits_map[plan_usage_limit_name])
            usage_limit.value = plan_usage_limit_value

            if usage_limit.value_type == ValueType.NUMERIC:
                if not isinstance(usage_limit.value, (int, float)):
                    raise InvalidDefaultValueException(
                        f"The usage limit {plan_usage_limit_name} does not have a valid value. Current valueType: {usage_limit.value_type}; Current value: {plan_usage_limit_value}")
            elif usage_limit.value_type == ValueType.BOOLEAN:
                if not isinstance(usage_limit.value, bool):
                    raise InvalidDefaultValueException(
                        f"The usage limit {plan_usage_limit_name} does not have a valid value. Current valueType: {usage_limit.value_type}; Current value: {plan_usage_limit_value}")
            elif usage_limit.value_type == ValueType.TEXT:
                if not isinstance(usage_limit.value, str):
                    raise InvalidDefaultValueException(
                        f"The usage limit {plan_usage_limit_name} does not have a valid value. Current valueType: {usage_limit.value_type}; Current value: {plan_usage_limit_value}")

            plan.usage_limits[plan_usage_limit_name] = usage_limit

    @staticmethod
    def parse_payment_value(feature: 'Feature', feature_name: str, map: Dict[str, Any]):
        payment_value = map.get("value")
        if isinstance(payment_value, str):
            raise PricingParsingException(f"{feature_name} should be a list of supported payment types")

        allowed_payment_types = payment_value
        for type_ in allowed_payment_types:
            if type_ not in PaymentType.__members__:
                raise InvalidDefaultValueException(
                    f"The feature {feature_name} does not have a supported paymentType. PaymentType that generates the issue: {type_}")
        feature.value = allowed_payment_types

    @staticmethod
    def is_valid_price(price: Any) -> bool:
        return isinstance(price, (int, float, str)) or price is None
