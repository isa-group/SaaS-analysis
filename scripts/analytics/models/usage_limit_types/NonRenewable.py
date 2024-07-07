from models import UsageLimit, UsageLimitType

class NonRenewable(UsageLimit):
    def __init__(self):
        super().__init__()
        self.type = UsageLimitType.NON_RENEWABLE

    def __str__(self):
        return f"NonRenewable[valueType: {self.value_type}, defaultValue: {self.default_value}, value: {self.value}, linkedFeature: {self.linked_features}]"