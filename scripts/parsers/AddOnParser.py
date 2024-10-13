from typing import Dict, Any
from scripts.models import AddOn, PricingManager, ValueType, UsageLimit, Feature
from scripts.models.feature_types import Payment
from scripts.parsers.exceptions import PricingParsingException, InvalidPlanException, FeatureNotFoundException, InvalidDefaultValueException
from .FeatureParser import FeatureParser

class AddOnParser:
    @staticmethod
    def parse_map_to_addon(addon_name: str, addon_map: Dict[str, Any], pricing_manager: 'PricingManager') -> 'AddOn':
        if addon_name is None:
            raise PricingParsingException("An add-on name cannot be null")

        addon = AddOn()
        addon.name = addon_name
        AddOnParser.set_available_for(addon_map, pricing_manager, addon)

        if "price" in addon_map and ("monthlyPrice" in addon_map or "annualPrice" in addon_map):
            raise PricingParsingException(f"The add-on {addon_name} has both a price and monthlyPrice/annualPrice. It should have only one of them")

        if "price" in addon_map:
            if AddOnParser.is_valid_price(addon_map["price"]):
                addon.price = addon_map["price"]
            else:
                raise PricingParsingException(f"The price of the add-on {addon_name} is neither a valid number nor string")

        if "monthlyPrice" in addon_map and "annualPrice" in addon_map:
            if AddOnParser.is_valid_price(addon_map["monthlyPrice"]) and AddOnParser.is_valid_price(addon_map["annualPrice"]):
                addon.monthly_price = addon_map["monthlyPrice"]
                addon.annual_price = addon_map["annualPrice"]
            else:
                raise PricingParsingException(f"The monthly or annual price of the add-on {addon_name} is neither a valid number nor string")

        AddOnParser.parse_addon_features(addon_map, addon, pricing_manager)
        AddOnParser.parse_addon_usage_limits(addon_map, addon, pricing_manager, False)
        AddOnParser.parse_addon_usage_limits(addon_map, addon, pricing_manager, True)

        return addon
    
    @staticmethod
    def populate_addons_dependencies(pricingManager: 'PricingManager', addons_map: Dict[str, 'AddOn']):
        for name in pricingManager.add_ons.keys():
            AddOnParser.set_depends_on(name, addons_map[name], pricingManager)

    @staticmethod
    def set_available_for(addon_map: Dict[str, Any], pricing_manager: 'PricingManager', addon: 'AddOn'):
        if "availableFor" in addon_map:
            plans = addon_map["availableFor"]
            for plan_name in plans:
                if plan_name not in pricing_manager.plans:
                    raise InvalidPlanException(f"The plan {plan_name} does not exist in the pricing manager")
            addon.available_for = plans
        else:
            addon.available_for = list(pricing_manager.plans.keys())

    @staticmethod
    def set_depends_on(addon_name: str, addon_map: Dict[str, Any], pricing_manager: 'PricingManager'):
        if "dependsOn" in addon_map.keys():
            required_addons = addon_map["dependsOn"]
            for required_addon in required_addons:
                if required_addon not in pricing_manager.add_ons:
                    raise InvalidPlanException(f"The addon {required_addon} does not exist in the pricing manager")
                if required_addon == addon_name:
                    raise InvalidPlanException(f"The addon {required_addon} cannot depend on itself")
            pricing_manager.add_ons[addon_name].depends_on = required_addons
        else:
            pricing_manager.add_ons[addon_name].depends_on = []

    @staticmethod
    def parse_addon_features(addon_map: Dict[str, Any], addon: 'AddOn', pricing_manager: 'PricingManager'):
        global_features_map = pricing_manager.features
        addon_features_map = addon_map.get("features", {})
        addon_features = {}

        for addon_feature_name, addon_feature_value in addon_features_map.items():
            if addon_feature_name not in global_features_map:
                raise FeatureNotFoundException(f"The feature {addon_feature_name} is not defined in the global features")

            feature = Feature.clone_feature(global_features_map[addon_feature_name])
            feature.value = addon_feature_value.get("value", addon_feature_value)

            if feature.value_type == ValueType.NUMERIC:
                if not isinstance(feature.value, (int, float)):
                    raise InvalidDefaultValueException(f"The feature {addon_feature_name} does not have a valid value. Current valueType: {feature.value_type}; Current value in {addon.name}: {addon_feature_value}")
            elif feature.value_type == ValueType.BOOLEAN:
                if not isinstance(feature.value, bool):
                    raise InvalidDefaultValueException(f"The feature {addon_feature_name} does not have a valid value. Current valueType: {feature.value_type}; Current value in {addon.name}: {addon_feature_value}")
            elif feature.value_type == ValueType.TEXT:
                if isinstance(feature, Payment):
                    FeatureParser.parse_payment_value(feature)
                if not isinstance(feature.value, str):
                    raise InvalidDefaultValueException(f"The feature {addon_feature_name} does not have a valid value. Current valueType: {feature.value_type}; Current value in {addon.name}: {addon_feature_value}")

            addon_features[addon_feature_name] = feature

        addon.features = addon_features

    @staticmethod
    def parse_addon_usage_limits(addon_map: Dict[str, Any], addon: 'AddOn', pricing_manager: 'PricingManager', are_extensions: bool):
        global_usage_limits_map = pricing_manager.usage_limits
        key = "usageLimitExtensions" if are_extensions else "usageLimits"
        addon_usage_limits_map = addon_map.get(key, {})
        addon_usage_limits = {}

        for addon_usage_limit_name, addon_usage_limit_value in addon_usage_limits_map.items():
            if addon_usage_limit_name not in global_usage_limits_map:
                raise FeatureNotFoundException(f"The feature {addon_usage_limit_name} is not defined in the global features")

            usage_limit = UsageLimit.clone_usage_limit(global_usage_limits_map[addon_usage_limit_name])
            usage_limit.value = addon_usage_limit_value.get("value", addon_usage_limit_value)

            if usage_limit.value_type == ValueType.NUMERIC:
                if not isinstance(usage_limit.value, (int, float)):
                    raise InvalidDefaultValueException(f"The usage limit {addon_usage_limit_name} does not have a valid value. Current valueType: {usage_limit.value_type}; Current value: {addon_usage_limit_value}")
            elif usage_limit.value_type == ValueType.BOOLEAN:
                if not isinstance(usage_limit.value, bool):
                    raise InvalidDefaultValueException(f"The usage limit {addon_usage_limit_name} does not have a valid value. Current valueType: {usage_limit.value_type}; Current value: {addon_usage_limit_value}")
            elif usage_limit.value_type == ValueType.TEXT:
                if not isinstance(usage_limit.value, str):
                    raise InvalidDefaultValueException(f"The usage limit {addon_usage_limit_name} does not have a valid value. Current valueType: {usage_limit.value_type}; Current value: {addon_usage_limit_value}")

            addon_usage_limits[addon_usage_limit_name] = usage_limit

        if are_extensions:
            addon.usage_limits_extensions = addon_usage_limits
        else:
            addon.usage_limits = addon_usage_limits

    @staticmethod
    def is_valid_price(price: Any) -> bool:
        return isinstance(price, (int, float, str))
