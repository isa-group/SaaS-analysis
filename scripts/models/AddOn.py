from typing import List, Dict, Optional, Any
from scripts.models import Feature, UsageLimit

class AddOn:
    def __init__(self, name: str = None, available_for: List[str] = None, price: Optional[Any] = None,
                 monthly_price: Optional[Any] = None, annual_price: Optional[Any] = None, unit: str = None,
                 features: Optional[Dict[str, 'Feature']] = None, usage_limits: Optional[Dict[str, 'UsageLimit']] = None,
                 usage_limits_extensions: Optional[Dict[str, 'UsageLimit']] = None):
        self.name = name
        self.available_for = available_for
        self.price = price
        self.monthly_price = monthly_price
        self.annual_price = annual_price
        self.unit = unit
        self.features = features if features is not None else {}
        self.usage_limits = usage_limits if usage_limits is not None else {}
        self.usage_limits_extensions = usage_limits_extensions if usage_limits_extensions is not None else {}

    def serialize_addon(self) -> Dict[str, Any]:
        serialized_addon = {}

        if self.available_for:
            serialized_addon["availableFor"] = self.available_for

        if self.price is not None:
            serialized_addon["price"] = self.price

        if self.monthly_price is not None:
            serialized_addon["monthlyPrice"] = self.monthly_price

        if self.annual_price is not None:
            serialized_addon["annualPrice"] = self.annual_price

        if self.unit is not None:
            serialized_addon["unit"] = self.unit

        features = self.serialize_features()
        usage_limits = self.serialize_usage_limits()
        usage_limit_extensions = self.serialize_usage_limit_extensions()

        serialized_addon["features"] = features
        serialized_addon["usageLimits"] = usage_limits
        serialized_addon["usageLimitExtensions"] = usage_limit_extensions

        return serialized_addon

    def serialize_value(self, value: Any) -> Optional[Dict[str, Any]]:
        if value is None:
            return None

        return {"value": value}

    def serialize_features(self) -> Optional[Dict[str, Any]]:
        if not self.features:
            return None

        serialized_features = {}
        for feature in self.features.values():
            serialized_feature = feature.serializeFeature()
            if serialized_feature:
                serialized_features[feature.name] = serialized_feature

        if not serialized_features:
            return None

        return serialized_features

    def serialize_usage_limits(self) -> Optional[Dict[str, Any]]:
        if not self.usage_limits:
            return None

        serialized_usage_limits = {}
        for usage_limit in self.usage_limits.values():
            serialized_usage_limit = self.serialize_value(usage_limit.getValue())
            if serialized_usage_limit:
                serialized_usage_limits[usage_limit.name] = serialized_usage_limit

        if not serialized_usage_limits:
            return None

        return serialized_usage_limits

    def serialize_usage_limit_extensions(self) -> Optional[Dict[str, Any]]:
        if not self.usage_limits_extensions:
            return None

        serialized_usage_limit_extensions = {}
        for usage_limit_extension in self.usage_limits_extensions.values():
            serialized_usage_limit_extension = self.serialize_value(usage_limit_extension.getValue())
            if serialized_usage_limit_extension:
                serialized_usage_limit_extensions[usage_limit_extension.name] = serialized_usage_limit_extension

        if not serialized_usage_limit_extensions:
            return None

        return serialized_usage_limit_extensions
