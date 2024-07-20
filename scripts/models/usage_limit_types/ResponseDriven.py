from scripts.models import UsageLimit, UsageLimitType

class ResponseDriven(UsageLimit):
    def __init__(self):
        super().__init__()
        self.type = UsageLimitType.RESPONSE_DRIVEN

    def __str__(self):
        return f"ResponseDriven[valueType: {self.value_type}, defaultValue: {self.default_value}, value: {self.value}, linkedFeature: {self.linked_features}]"
