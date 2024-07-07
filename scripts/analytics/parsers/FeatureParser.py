from typing import Dict, Any
from models import ValueType, Feature, FeatureType
from models.feature_types import Information, Integration, Domain, Automation, Management, Guarantee, Support, Payment, AutomationType, IntegrationType, PaymentType
from parsers.exceptions import PricingParsingException, InvalidDefaultValueException

class FeatureParser:
    @staticmethod
    def parse_map_to_feature(feature_name: str, feature_map: Dict[str, Any]) -> 'Feature':
        feature_type = FeatureType(feature_map["type"])

        if feature_type == FeatureType.INFORMATION:
            return FeatureParser.parse_map_to_information(feature_name, feature_map)
        elif feature_type == FeatureType.INTEGRATION:
            return FeatureParser.parse_map_to_integration(feature_name, feature_map)
        elif feature_type == FeatureType.DOMAIN:
            return FeatureParser.parse_map_to_domain(feature_name, feature_map)
        elif feature_type == FeatureType.AUTOMATION:
            return FeatureParser.parse_map_to_automation(feature_name, feature_map)
        elif feature_type == FeatureType.MANAGEMENT:
            return FeatureParser.parse_map_to_management(feature_name, feature_map)
        elif feature_type == FeatureType.GUARANTEE:
            return FeatureParser.parse_map_to_guarantee(feature_name, feature_map)
        elif feature_type == FeatureType.SUPPORT:
            return FeatureParser.parse_map_to_support(feature_name, feature_map)
        elif feature_type == FeatureType.PAYMENT:
            return FeatureParser.parse_map_to_payment(feature_name, feature_map)
        else:
            raise ValueError(f"Unknown feature type: {feature_type}")

    @staticmethod
    def parse_map_to_information(feature_name: str, feature_map: Dict[str, Any]) -> 'Information':
        information = Information()
        information.name = feature_name
        FeatureParser.set_common_fields(information, feature_name, feature_map)
        return information

    @staticmethod
    def parse_map_to_integration(feature_name: str, feature_map: Dict[str, Any]) -> 'Integration':
        integration = Integration()
        integration.name = feature_name
        integration.integration_type = IntegrationType(feature_map["integrationType"])
        FeatureParser.set_common_fields(integration, feature_name, feature_map)
        return integration

    @staticmethod
    def parse_map_to_domain(feature_name: str, feature_map: Dict[str, Any]) -> 'Domain':
        domain = Domain()
        domain.name = feature_name
        FeatureParser.set_common_fields(domain, feature_name, feature_map)
        return domain

    @staticmethod
    def parse_map_to_automation(feature_name: str, feature_map: Dict[str, Any]) -> 'Automation':
        automation = Automation()
        automation.name = feature_name
        automation.automation_type = AutomationType(feature_map["automationType"])
        FeatureParser.set_common_fields(automation, feature_name, feature_map)
        return automation

    @staticmethod
    def parse_map_to_management(feature_name: str, feature_map: Dict[str, Any]) -> 'Management':
        management = Management()
        management.name = feature_name
        FeatureParser.set_common_fields(management, feature_name, feature_map)
        return management

    @staticmethod
    def parse_map_to_guarantee(feature_name: str, feature_map: Dict[str, Any]) -> 'Guarantee':
        guarantee = Guarantee()
        guarantee.name = feature_name
        FeatureParser.set_common_fields(guarantee, feature_name, feature_map)
        return guarantee

    @staticmethod
    def parse_map_to_support(feature_name: str, feature_map: Dict[str, Any]) -> 'Support':
        support = Support()
        support.name = feature_name
        FeatureParser.set_common_fields(support, feature_name, feature_map)
        return support

    @staticmethod
    def parse_map_to_payment(feature_name: str, feature_map: Dict[str, Any]) -> 'Payment':
        payment = Payment()
        payment.name = feature_name
        FeatureParser.set_common_fields(payment, feature_name, feature_map)
        FeatureParser.parse_payment_value(payment, feature_name, feature_map)
        return payment

    @staticmethod
    def set_common_fields(feature: 'Feature', feature_name: str, feature_map: Dict[str, Any]):
        feature.description = feature_map.get("description")
        feature.value_type = ValueType(feature_map["valueType"])

        try:
            if feature.value_type == ValueType.NUMERIC:
                feature.default_value = feature_map["defaultValue"]
                if not isinstance(feature.default_value, (int, float)):
                    raise InvalidDefaultValueException(
                        f"The feature {feature_name} does not have a valid defaultValue. Current valueType: {feature.value_type}; Current defaultValue: {feature_map['defaultValue']}")
            elif feature.value_type == ValueType.BOOLEAN:
                feature.default_value = bool(feature_map["defaultValue"])
            elif feature.value_type == ValueType.TEXT:
                if isinstance(feature, Payment):
                    FeatureParser.parse_payment_value(feature, feature_name, feature_map)
                else:
                    feature.default_value = str(feature_map["defaultValue"])
        except KeyError as e:
            raise InvalidDefaultValueException(f"Missing required field in feature {feature_name}: {str(e)}")

        try:
            if "expression" not in feature_map:
                feature.expression = None
            else:
                feature.expression = feature_map["expression"]
            if "serverExpression" not in feature_map:
                feature.server_expression = None
            else:
                feature.server_expression = feature_map["serverExpression"]
        except KeyError as e:
            raise PricingParsingException(f"The feature {feature_name} does not have either an evaluation expression or serverExpression.")

    @staticmethod
    def parse_payment_value(feature: 'Feature', feature_name: str, feature_map: Dict[str, Any]):
        allowed_payment_types = feature_map["defaultValue"]
        for type_ in allowed_payment_types:
            if type_ not in PaymentType.__members__:
                raise InvalidDefaultValueException(
                    f"The feature {feature_name} does not have a supported paymentType. PaymentType that generates the issue: {type_}")
        feature.default_value = allowed_payment_types
