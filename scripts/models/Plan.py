from typing import Dict, Optional, Any
from scripts.models import Feature, UsageLimit

class Plan:
    def __init__(self, name: str = None, description: Optional[str] = None, monthly_price: Optional[Any] = None,
                 annual_price: Optional[Any] = None, unit: str = None, features: Optional[Dict[str, 'Feature']] = None,
                 usage_limits: Optional[Dict[str, 'UsageLimit']] = None):
        self.name = name
        self.description = description
        self.monthly_price = monthly_price
        self.annual_price = annual_price
        self.unit = unit
        self.features = features if features is not None else {}
        self.usage_limits = usage_limits if usage_limits is not None else {}

    def parse_to_map(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "monthlyPrice": self.monthly_price,
            "annualPrice": self.annual_price,
            "unit": self.unit,
            "features": self.features,
            "usageLimits": self.usage_limits
        }

    def serialize_plan(self) -> Dict[str, Any]:
        attributes = {
            "description": self.description,
            "monthlyPrice": self.monthly_price,
            "annualPrice": self.annual_price,
            "unit": self.unit
        }

        features = self.serialize_features()
        usage_limits = self.serialize_usage_limits()

        attributes["features"] = features
        attributes["usageLimits"] = usage_limits

        return attributes

    def serialize_value(self, value: Any) -> Optional[Dict[str, Any]]:
        if value is None:
            return None
        return {"value": value}

    def serialize_features(self) -> Optional[Dict[str, Any]]:
        if not self.features:
            return None

        serialized_features = {}
        for feature in self.features.values():
            serialized_feature = self.serialize_value(feature.get_value())
            if serialized_feature:
                serialized_features[feature.get_name()] = serialized_feature

        if not serialized_features:
            return None

        return serialized_features

    def serialize_usage_limits(self) -> Optional[Dict[str, Any]]:
        if not self.usage_limits:
            return None

        serialized_usage_limits = {}
        for usage_limit in self.usage_limits.values():
            serialized_usage_limit = self.serialize_value(usage_limit.get_value())
            if serialized_usage_limit:
                serialized_usage_limits[usage_limit.get_name()] = serialized_usage_limit

        if not serialized_usage_limits:
            return None

        return serialized_usage_limits

    def __str__(self) -> str:
        super_admin_role = self.features.get("superAdminRole", "None")
        return f"Plan[name={self.name}, monthlyPrice={self.monthly_price}, annualPrice={self.annual_price}, unit={self.unit}, features: {super_admin_role}]"
