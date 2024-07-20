import copy
from typing import List, Dict, Optional, Any


class CloneUsageLimitException(Exception):
    pass


class ValueType:
    # Placeholder for the actual ValueType implementation
    def __str__(self):
        return "ValueTypeString"


class UsageLimitType:
    # Placeholder for the actual UsageLimitType implementation
    def __str__(self):
        return "UsageLimitTypeString"


class UsageLimit:
    def __init__(self, name: str = None, description: Optional[str] = None, value_type: ValueType = None,
                 default_value: Any = None, unit: str = None, value: Optional[Any] = None, 
                 linked_features: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.value_type = value_type
        self.default_value = default_value
        self.unit = unit
        self.value = value
        self.linked_features = linked_features if linked_features is not None else []

    def is_linked_to_feature(self, feature_name: str) -> bool:
        return feature_name in self.linked_features

    def serialize(self) -> Dict[str, Any]:
        attributes = {}

        if self.description is not None:
            attributes["description"] = self.description

        if self.value_type is not None:
            attributes["valueType"] = str(self.value_type)

        if self.default_value is not None:
            attributes["defaultValue"] = self.default_value

        if self.unit is not None:
            attributes["unit"] = self.unit

        attributes["type"] = str(self.type)

        if self.linked_features:
            attributes["linkedFeatures"] = self.linked_features

        if self.expression is not None:
            attributes["expression"] = self.expression

        if self.server_expression is not None:
            attributes["serverExpression"] = self.server_expression

        return attributes

    @staticmethod
    def clone_usage_limit(original: 'UsageLimit') -> 'UsageLimit':
        try:
            return copy.deepcopy(original)
        except Exception as e:
            raise CloneUsageLimitException("Error cloning usageLimit") from e
