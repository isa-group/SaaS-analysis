from enum import Enum

class PaymentType(Enum):
    CARD = "CARD"
    GATEWAY = "GATEWAY"
    INVOICE = "INVOICE"
    ACH = "ACH"
    WIRE_TRANSFER = "WIRE_TRANSFER"
    OTHER = "OTHER"
