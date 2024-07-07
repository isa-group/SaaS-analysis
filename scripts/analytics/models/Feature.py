import copy
from typing import Dict, Optional, Any
from models import ValueType
from models.exceptions import CloneFeatureException

class Feature:
    def __init__(self, name: str = None, description: Optional[str] = None, value_type: ValueType = None,
                 default_value: Any = None, value: Optional[Any] = None, expression: Optional[str] = None,
                 server_expression: Optional[str] = None):
        self.name = name
        self.description = description
        self.value_type = value_type
        self.default_value = default_value
        self.value = value
        self.expression = expression
        self.server_expression = server_expression

    def prepare_to_plan_writing(self):
        self.name = None
        self.value = None
        self.description = None
        self.default_value = None
        self.expression = None
        self.server_expression = None

    def has_overwritten_default_value(self) -> bool:
        return self.default_value != self.value

    def feature_attributes_map(self) -> Dict[str, Any]:
        attributes = {}

        if self.description is not None:
            attributes["description"] = self.description

        if self.value_type is not None:
            attributes["valueType"] = str(self.value_type)

        if self.default_value is not None:
            attributes["defaultValue"] = self.default_value

        if self.expression is not None:
            attributes["expression"] = self.expression

        if self.server_expression is not None:
            attributes["serverExpression"] = self.server_expression

        return attributes

    def serialize_feature(self) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses should implement this method.")

    @staticmethod
    def clone_feature(original: 'Feature') -> 'Feature':
        try:
            return copy.deepcopy(original)
        except Exception as e:
            raise CloneFeatureException("Error cloning feature") from e
