from scripts.PricingsLoader import PricingsLoader
from tqdm import tqdm
import os

dataset = PricingsLoader('./pricings/yaml')

if __name__ == '__main__':
    test = 0
    for i in tqdm(range(len(dataset))):
        path = dataset.get_path(i)
        
        dzn_path = path.replace('/yaml/', '/dzn/').replace('.yml', '.dzn')
        
        with open(dzn_path, 'r') as file:
            content = file.read()
            
            # If content doesn't containt "addons_depends_on", remove de file
            if 'addons_depends_on' not in content:
                os.remove(dzn_path)