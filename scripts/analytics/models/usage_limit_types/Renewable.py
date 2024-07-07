from models import UsageLimit, UsageLimitType

class Renewable(UsageLimit):
    def __init__(self):
        super().__init__()
        self.type = UsageLimitType.RENEWABLE

    def __str__(self):
        return f"Renewable[valueType: {self.value_type}, defaultValue: {self.default_value}, value: {self.value}, linkedFeature: {self.linked_features}]"
