import json
import os
import hashlib

data_dir = './data/'

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def m_tree(transactions):
    """Takes an array of transactions and computes a Merkle root"""
    sub_t = []
    for i in chunks(transactions,2):
        if len(i) == 2:
            hash =  hashlib.sha256(str(i[0]+i[1])).hexdigest()
        else:
            hash =  hashlib.sha256(str(i[0]+i[0])).hexdigest()
        sub_t.append(hash)
    if len(sub_t) == 1:
       return sub_t[0]
    else:
       return m_tree(sub_t)

def calculate_markel_root(data):
    transactions = []
    for elem in data:
        transactions.append(elem["transaction_id"])
    markel_root = m_tree(transactions)
    return markel_root


def check_block(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    blockhash = data["header"]["blockhash"]
    del data["header"]["blockhash"]
    if blockhash != hashlib.sha256(json.dumps(data["header"])).hexdigest():
        return False
    markel_root = data["header"]["markel_root"]
    transactions = data["transactions"]
    calculated_markel_root = calculate_markel_root(transactions)
    if calculated_markel_root == markel_root:
        return True



if __name__ == "__main__":
    for blk_file in os.listdir(data_dir):
        print check_block(os.path.join(data_dir, blk_file))
