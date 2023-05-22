from datetime import datetime
from op_aes import *
from op_json import *
import hashlib

# Function to calculate the hash of a block
def calculate_hash(data):
    # You can implement your hash calculation logic here
    data_string = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(data_string).hexdigest()

# Create an empty list to store the blocks


# Create a function to add a new block to the blockchain
def add_block_encrypted(patient_id, name, medical_data, encryption_key):
    # Encrypt the medical data
    encrypted_medical_data = encrypt_data(encryption_key, json.dumps(medical_data))

    # Create a new block dictionary
    block = {
        "patient_id": patient_id,
        "name": name,
        "medical_data": encrypted_medical_data.hex(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "previous_hash": None
    }

    return block

def add_block_decrypted(patient_id, name, medical_data, encryption_key):
    # Encrypt the medical data
    decrypted_medical_data = decrypt_data(encryption_key, json.dumps(medical_data))

    # Create a new block dictionary
    block = {
        "patient_id": patient_id,
        "name": name,
        "medical_data": decrypted_medical_data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "previous_hash": None
    }

    return block

# Create a function to add a new block to the blockchain
def add_block(patient_id, name, medical_data):

    # Create a new block dictionary
    block = {
        "patient_id": patient_id,
        "name": name,
        "medical_data": medical_data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "previous_hash": None
    }

    return block

def add_hash(blockchain, block):
    # Calculate the hash of the previous block
    if len(blockchain) > 0:
        previous_block = blockchain[-1]
        block["previous_hash"] = calculate_hash(previous_block)

    # Calculate the hash of the current block
    block["hash"] = calculate_hash(block)

    # Append the block to the blockchain
    blockchain.append(block)
    return blockchain


