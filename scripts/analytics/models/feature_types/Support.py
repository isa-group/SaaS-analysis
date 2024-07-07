from typing import Dict, Any, Optional
from models import Feature, FeatureType, ValueType

class Support(Feature):

    def __init__(self, name: str = None, description: Optional[str] = None, value_type: ValueType = None,
                 default_value: Any = None, value: Optional[Any] = None, expression: Optional[str] = None,
                 server_expression: Optional[str] = None):
        super().__init__(name, description, value_type, default_value, value, expression, server_expression)

    def serialize_feature(self) -> Dict[str, Any]:
        attributes = self.feature_attributes_map()
        attributes["type"] = FeatureType.SUPPORT.value
        return attributes

    def __str__(self):
        return (f"Support[name: {self.name}, valueType: {self.value_type}, defaultValue: {self.default_value}, "
                f"value: {self.value}]")
