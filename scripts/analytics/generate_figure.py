from dataset_generator import PricingsLoader

if __name__ == '__main__':
    
    dataset = PricingsLoader('pricings')

    print(len(dataset))

    evernote = dataset.find_pricing('evernote', 2020)
    test = dataset[0]

    print(evernote)
    print("------------------")
    print(test)