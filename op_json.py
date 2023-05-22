import json
import os

# Function to save blockchain to a JSON file
def save_blockchain_to_json(blockchain, filename):
    #filepath = os.path.join(os.getcwd(), filename)  # Get the current working directory and join it with the filename
    if blockchain:
        filtered_blockchain = [block for block in blockchain if block is not None]
        json_blockchain = json.dumps(filtered_blockchain, indent=4)
        with open(filename, 'w') as file:
            file.write(json_blockchain)
        print(f"Blockchain saved to {filename}")
    else:
        print("Blockchain is empty. Nothing to save.")

# Function to load blockchain from a JSON file
def load_blockchain_from_json(filename, block_class):
    filepath = os.path.join(os.getcwd(), filename)  # Get the current working directory and join it with the filename
    with open(filepath, "r") as file:
        json_data = file.read()
    blockchain = [block_class(**block) for block in json.loads(json_data)]
    return blockchain

def load_json(filename): 
    filename = filename.rstrip('\n')
    with open(filename, "r") as file:
        data = json.load(file)
    return data

def load_and_print_json(filename):
    filepath = os.path.join(os.getcwd(), filename)
    with open(filename, "r") as file:
        data = json.load(file)
    print(json.dumps(data, indent=4))

