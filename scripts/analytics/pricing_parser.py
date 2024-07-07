import yaml
from parsers import PricingManagerParser

def parse_pricing(path):
    pricing_dict = None

    with open(path, 'r') as file:
        pricing_dict = yaml.safe_load(file)
    
    def remove_none_values(d):
        if isinstance(d, dict):
            return {k: remove_none_values(v) for k, v in d.items() if v is not None}
        else:
            return d
    
    clean_dict = remove_none_values(pricing_dict)

    pricing = PricingManagerParser.parse_map_to_pricing_manager(clean_dict)

    return pricing