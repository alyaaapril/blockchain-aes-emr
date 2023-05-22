from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
from op_blockchain import *
from op_json import *
from op_aes import *

import tkinter as tk
from tkinter import ttk


##-------------------------------FUNGSI REUSABLE-------------------------------------------- 
def browse_file(label):
    # ambil path
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = ( ("JSON files",
                                                         "*.json*"), 
                                                         ( "Text files",
                                                        "*.txt*"), 
                                                        ("JPG files",
                                                        "*.jpg*"),
                                                        ("JPEG files",
                                                        "*.jpeg*"),
                                                       ("all files",
                                                        "*.*"),
                                                        ))
    label.insert(END, filename)
    return(filename)
    
def browse_file_json():
    browse_file(entry_file)

def browse_file_json2():
    browse_file(entry_file2)

def save_key(key):
    file_name = filedialog.asksaveasfile(defaultextension=".txt").name
    try:
        f = open(file_name, 'w')
        f.write(str(key))
        f.close()
        showinfo("Info", "Key berhasil disimpan")
    except:
        raise(Exception('File not found and can not be opened:', file_name))


def generate_save_key():
    key = encryption_key()
    save_key(key)

def browse_key(label):
    filename = filedialog.askopenfilename(defaultextension=".txt")
    # show directory
    label.insert(END, filename)

def browse_encryption_key():
    browse_key(entry_gen_k)

def browse_encryption_key2():
    browse_key(entry_gen_k2)

def read_key(filename):
    filename = filename.rstrip('\n')
    with open(filename, 'rb') as file:
        key = file.read(32)  # Read 32 bytes from the file
    return key

def read_file_json(filename):
    input_data = load_json(filename)
    return input_data

def print_key():
    print(read_key(entry_gen_k.get("1.0", tk.END)))

def clear_text():
    entry_gen_k.delete('1.0', END)
    entry_file.delete('1.0', END)

def clear_text2():
    entry_gen_k2.delete('1.0', END)
    entry_file2.delete('1.0', END)


def blockchain():
    #input_data = entry_file.get("1.0", tk.END)
    input_data = read_file_json(entry_file.get("1.0", tk.END))
    blockchain = []
    for data in input_data:
        patient_id = data["patient_id"]
        name = data["name"]
        medical_data = data["medical_data"]
        add_hash(blockchain, add_block(patient_id, name, medical_data))
    save_blockchain_to_json(blockchain, "blockchain_without_encrypt.json")

def blockchain_aes():
    encrypt_key = read_key(entry_gen_k.get("1.0", tk.END))
    #input_data = entry_file.get("1.0", tk.END)
    input_data = read_file_json(entry_file.get("1.0", tk.END))
    blockchain_encrypted = []
    for data in input_data:
        patient_id = data["patient_id"]
        name = data["name"]
        medical_data = data["medical_data"]
        add_hash(blockchain_encrypted, add_block_encrypted(patient_id, name, medical_data, encrypt_key))
    save_blockchain_to_json(blockchain_encrypted, "blockchain_encrypted.json")

def blockchain_decrypted():
    encrypt_key = read_key(entry_gen_k2.get("1.0", tk.END))
    input_data = read_file_json(entry_file2.get("1.0", tk.END))
    blockchain_decrypted = []
    for data in input_data:
        patient_id = data["patient_id"]
        name = data["name"]
        medical_data = data["medical_data"]
        add_hash(blockchain_decrypted, add_block_decrypted(patient_id, name, medical_data, encrypt_key))
    save_blockchain_to_json(blockchain_decrypted, "blockchain_decrypted.json")

root = tk.Tk()
root.title("Rekam Medis Elektronik")
root.geometry("800x600")

notebook = ttk.Notebook(root)

## TAB 1 (Pembuatan Blockchain)
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Generate Blockchain")
title1 = tk.Label(tab1, text="Blockchain", font= ('arial', 15))
title1.grid(row=0, column=0, padx=5, pady=5)

btn_save_key = tk.Button(tab1, height=1, width=50, text="Generate Key (AES 256)",  font = ('arial ', 10), fg="black", bg="#D3C3B1", command=generate_save_key)
btn_save_key.grid(row=1, column=1, pady=1)

label_gen_k = tk.Label(tab1, text = 'Your Key:', font = ('Inter ', 10))
label_gen_k.grid(row=2, column=0, padx=10, pady=5, stick='e')

entry_gen_k = tk.Text(tab1, width = 52)
entry_gen_k.grid(row=2, column=1, stick='w', padx=20, pady=10)
entry_gen_k.config(height = 1)

btn_generate_k = tk.Button(tab1, 
                           height=1, width=10, text="Upload",  
                           font = ('arial ', 10), fg="black", bg="#D3C3B1", 
                           command=browse_encryption_key)
btn_generate_k.grid(row=2, column=2, pady=1)


# LOAD FILE
btn_load_file = tk.Button(tab1, height=3, width=10, text="Load Json File",  font = ('arial ', 10), fg="black", bg="#D3C3B1", command=browse_file_json)
btn_load_file.grid(row=4, column=0, pady=0)

entry_file = tk.Text(tab1, width = 52)
entry_file.grid(row=4, column=1, stick='w', padx=20, pady=10)
entry_file.config(height = 15)

btn_save_blockchain = tk.Button(tab1, height=1, width=50, text="Develop Blockchain",  font = ('arial ', 10), fg="black", bg="#D3C3B1", command=blockchain)
btn_save_blockchain.grid(row=5, column=1, pady=1)

btn_save_blockchain_aes = tk.Button(tab1, height=1, width=50, text="Develop Encrypted Blockchain",  font = ('arial ', 10), fg="black", bg="#D3C3B1", command=blockchain_aes)
btn_save_blockchain_aes.grid(row=6, column=1, pady=1)

btn_clear = tk.Button(tab1, height=1, width=50, text="Delete File & Key",  font = ('arial ', 10), fg="black", bg="#D3C3B1", command=clear_text)
btn_clear.grid(row=7, column=1, pady=1)


## TAB 2 (Check Data Confidentiality)
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Check Data Confidentiality")
title2 = tk.Label(tab2, text="Confidential Data", font=('arial', 15))
title2.grid(row=0, column=0, padx=10, pady=10)

label_gen_k2 = tk.Label(tab2, text = 'Your Key:', font = ('Inter ', 10))
label_gen_k2.grid(row=1, column=0, padx=10, pady=5, stick='e')

entry_gen_k2 = tk.Text(tab2, width = 52)
entry_gen_k2.grid(row=1, column=1, stick='w', padx=20, pady=10)
entry_gen_k2.config(height = 1)

btn_generate_k2 = tk.Button(tab2, 
                           height=1, width=10, text="Upload",  
                           font = ('arial ', 10), fg="black", bg="#D3C3B1", 
                           command=browse_encryption_key2)
btn_generate_k2.grid(row=1, column=2, pady=1)


# LOAD FILE
btn_load_file2 = tk.Button(tab2, height=3, width=20, text="Load Json Blockchain File",  font = ('arial ', 10), fg="black", bg="#D3C3B1", command=browse_file_json2)
btn_load_file2.grid(row=2, column=0, pady=0)

entry_file2 = tk.Text(tab2, width = 52)
entry_file2.grid(row=2, column=1, stick='w', padx=20, pady=10)
entry_file2.config(height = 15)

btn_save_blockchain2 = tk.Button(tab2, height=1, width=50, text="Decrypt Confidential Data",  font = ('arial ', 10), fg="black", bg="#D3C3B1", command=blockchain_decrypted)
btn_save_blockchain2.grid(row=5, column=1, pady=1)

btn_clear2 = tk.Button(tab1, height=1, width=50, text="Delete File & Key",  font = ('arial ', 10), fg="black", bg="#D3C3B1", command=clear_text2)
btn_clear2.grid(row=7, column=1, pady=1)

# Pack the notebook widget and start the main loop
notebook.pack(expand=True, fill="both")
root.mainloop()