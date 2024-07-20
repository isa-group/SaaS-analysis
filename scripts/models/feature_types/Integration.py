from typing import Dict, Any, Optional
from scripts.models import Feature, FeatureType, ValueType
from scripts.models.feature_types import IntegrationType

class Integration(Feature):

    def __init__(self, name: str = None, description: Optional[str] = None, value_type: ValueType = None,
                 default_value: Any = None, value: Optional[Any] = None, expression: Optional[str] = None,
                 server_expression: Optional[str] = None, integration_type: Optional['IntegrationType'] = None):
        super().__init__(name, description, value_type, default_value, value, expression, server_expression)
        self.integration_type = integration_type

    def serialize_feature(self) -> Dict[str, Any]:
        attributes = self.feature_attributes_map()
        attributes["type"] = FeatureType.INTEGRATION.value
        return attributes

    def __str__(self):
        return (f"Integration[name: {self.name}, valueType: {self.value_type}, defaultValue: {self.default_value}, "
                f"value: {self.value}]")
