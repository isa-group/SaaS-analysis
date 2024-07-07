import yaml
from parsers import PricingManagerParser

def parse_pricing(path):
    pricing_dict = None

    with open(path, 'r') as file:
        pricing_dict = yaml.safe_load(file)

    pricing = PricingManagerParser.parse_map_to_pricing_manager(pricing_dict)

    return pricing