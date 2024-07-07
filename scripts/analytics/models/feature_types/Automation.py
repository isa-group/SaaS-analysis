from typing import Dict, Optional, Any
from models import Feature, FeatureType, ValueType
from models.feature_types import AutomationType

class Automation(Feature):
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None, value_type: Optional[ValueType] = None,
                 default_value: Optional[Any] = None, value: Optional[Any] = None, expression: Optional[str] = None,
                 server_expression: Optional[str] = None, automation_type: Optional['AutomationType'] = None):
        super().__init__(name, description, value_type, default_value, value, expression, server_expression)
        self.automation_type = automation_type

    def serialize_feature(self) -> Dict[str, Any]:
        features_attributes = self.feature_attributes_map()
        features_attributes["type"] = FeatureType.AUTOMATION.value

        if self.automation_type:
            features_attributes["automationType"] = str(self.automation_type)

        return features_attributes

    def __str__(self):
        return (f"Automation[name: {self.name}, valueType: {self.value_type}, defaultValue: {self.default_value}, "
                f"value: {self.value}, automationType: {self.automation_type}]")
