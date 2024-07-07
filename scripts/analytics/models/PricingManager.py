from typing import Dict, List, Any
from models import Feature, UsageLimit, Plan, AddOn

class PricingManager:
    def __init__(self, saas_name: str, day: int, month: int, year: int, currency: str, has_annual_payment: bool,
                 features: Dict[str, 'Feature'] = None, usage_limits: Dict[str, 'UsageLimit'] = None,
                 plans: Dict[str, 'Plan'] = None, add_ons: Dict[str, 'AddOn'] = None, pricing_dict: Dict[str, Any] = None):
        self.saas_name = saas_name
        self.day = day
        self.month = month
        self.year = year
        self.currency = currency
        self.has_annual_payment = has_annual_payment
        self.features = features if features is not None else {}
        self.usage_limits = usage_limits if usage_limits is not None else {}
        self.plans = plans if plans is not None else {}
        self.add_ons = add_ons if add_ons is not None else {}
        self.pricing_dict = pricing_dict if pricing_dict is not None else {}

    def get_plan_names(self) -> List[str]:
        return list(self.plans.keys())

    def get_plan_usage_limits(self, plan_name: str) -> Dict[str, Any]:
        usage_limits_context = {}
        plan_usage_limits = self.plans.get(plan_name).usage_limits

        default_usage_limits = self.usage_limits

        for usage_limit_name in default_usage_limits.keys():
            default_usage_limit_value = self.usage_limits.get(usage_limit_name)
            plan_usage_limit_value = plan_usage_limits.get(usage_limit_name)
            current_value = plan_usage_limit_value if plan_usage_limit_value is not None else default_usage_limit_value
            usage_limits_context[usage_limit_name] = current_value

        return usage_limits_context

    def __str__(self) -> str:
        return str(self.pricing_dict)