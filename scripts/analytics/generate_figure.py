import pprint
from dataset_generator import PricingsLoader
import matplotlib.pyplot as plt

def generate_figure(dataset):

    x = [1, 1 , 2, 3]
    y = [1, 2, 3, 4]

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o', linestyle='-', color='b')

    plt.show()

if __name__ == '__main__':
    
    dataset = PricingsLoader('../../pricings')

    generate_figure(dataset)