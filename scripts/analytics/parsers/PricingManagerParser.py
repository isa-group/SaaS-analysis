from typing import Dict, Any
from models import PricingManager
from parsers.exceptions import PricingParsingException
from parsers import FeatureParser, PlanParser, AddOnParser
from .UsageLimitParser import UsageLimitParser
from .PlanParser import PlanParser
from .AddOnParser import AddOnParser
class PricingManagerParser:
    @staticmethod
    def parse_map_to_pricing_manager(yaml_config_map: Dict[str, Any]) -> 'PricingManager':
        pricing_manager = PricingManagerParser.generate_manager_with_basic_attributes(yaml_config_map)
        PricingManagerParser.set_features(yaml_config_map, pricing_manager)
        PricingManagerParser.set_usage_limits(yaml_config_map, pricing_manager)
        PricingManagerParser.set_plans(yaml_config_map, pricing_manager)
        PricingManagerParser.set_add_ons(yaml_config_map, pricing_manager)

        if not pricing_manager.plans and not pricing_manager.add_ons:
            raise PricingParsingException("The pricing manager does not have any plans or add-ons")

        return pricing_manager

    @staticmethod
    def generate_manager_with_basic_attributes(yaml_config_map: Dict[str, Any]) -> 'PricingManager':
        required_fields = ["saasName", "day", "month", "year", "currency"]
        for field in required_fields:
            if yaml_config_map.get(field) is None:
                raise PricingParsingException(f"{field.capitalize()} was not defined")

        saas_name = yaml_config_map["saasName"]
        day = yaml_config_map["day"]
        month = yaml_config_map["month"]
        year = yaml_config_map["year"]
        currency = yaml_config_map["currency"]
        has_annual_payment = yaml_config_map.get("hasAnnualPayment", False)

        pricing_manager = PricingManager(saas_name, day, month, year, currency, has_annual_payment, pricing_dict=yaml_config_map)

        return pricing_manager

    @staticmethod
    def set_features(yaml_config_map: Dict[str, Any], pricing_manager: 'PricingManager'):
        features_map = yaml_config_map.get("features", {})
        features = {name: FeatureParser.parse_map_to_feature(name, f_map) for name, f_map in features_map.items()}
        pricing_manager.features = features

    @staticmethod
    def set_usage_limits(yaml_config_map: Dict[str, Any], pricing_manager: 'PricingManager'):
        usage_limits_map = yaml_config_map.get("usageLimits", {})
        usage_limits = {name: UsageLimitParser.parse_map_to_usage_limit(name, ul_map, pricing_manager) for name, ul_map in usage_limits_map.items()}
        pricing_manager.usage_limits = usage_limits

    @staticmethod
    def set_plans(yaml_config_map: Dict[str, Any], pricing_manager: 'PricingManager'):
        plans_map = yaml_config_map.get("plans", {})
        plans = {name: PlanParser.parse_map_to_plan(name, p_map, pricing_manager) for name, p_map in plans_map.items()}
        pricing_manager.plans = plans

    @staticmethod
    def set_add_ons(yaml_config_map: Dict[str, Any], pricing_manager: 'PricingManager'):
        add_ons_map = yaml_config_map.get("addOns", {})
        add_ons = {name: AddOnParser.parse_map_to_addon(name, ao_map, pricing_manager) for name, ao_map in add_ons_map.items()}
        pricing_manager.add_ons = add_ons
