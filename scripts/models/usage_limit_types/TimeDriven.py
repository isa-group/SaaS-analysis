from scripts.models import UsageLimit, UsageLimitType

class TimeDriven(UsageLimit):
    def __init__(self):
        super().__init__()
        self.type = UsageLimitType.TIME_DRIVEN

    def __str__(self):
        return f"TimeDriven[valueType: {self.value_type}, defaultValue: {self.default_value}, value: {self.value}, linkedFeature: {self.linked_features}]"
