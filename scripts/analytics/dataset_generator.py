import os
import pandas as pd
from pricing_parser import parse_pricing

class PricingsLoader():
    def __init__(self, pricings_folder: str):
        self.pricings_folder = pricings_folder
        self.dataset = pd.DataFrame(columns=['name', 'year', 'path'])
        self._load_pricings()
    
    def find_pricing(self, name: str, year: int):
        dataset_entry = self.dataset[(self.dataset['name'] == name) & (self.dataset['year'] == str(year))]
        if dataset_entry.empty:
            return None
        return self._get_pricing(dataset_entry.index[0])

    def __len__(self):
        return len(self.dataset)
    
    def __getitem__(self, idx):
        return self._get_pricing(idx)

    def _get_pricing(self, idx):
        
        pricing_entry = self.dataset.iloc[idx]
        pricing = parse_pricing(pricing_entry['path'])

        return pricing

    def _load_pricings(self):

        years = list(filter(lambda x: os.path.isdir(os.path.join(self.pricings_folder, x)), os.listdir(self.pricings_folder)))
        for year in years:
            year_folder = os.path.join(self.pricings_folder, year)
            pricings = list(filter(lambda x: x.endswith('.yml'), os.listdir(year_folder)))

            for pricing in pricings:
                self.dataset.loc[len(self.dataset)] = {'name': pricing.replace(".yml", ""), 'year': year, 'path': os.path.join(year_folder, pricing)}