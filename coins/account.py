import hashlib
import csv
import time
import requests, json

block_chain_manager_url = "http://127.0.0.1:9000/manager/"

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
    

class Account:
    balance = 10 #every person starts with 10 coins
    def __init__(self,name,port=9501):
        self.port = port
        self.name = name
        self.hexcode = hashlib.sha256(name).hexdigest()
    def send(self,value):
        if self.balance >= value:
            self.balance = self.balance - value
            return True
        else:
            return False
    def recieve(self,value): #ideally reject value if -ve
        self.balance = self.balance + value


# should be a function not a class :p [my bad]
class Transaction:
    def __init__(self,personSending,personReciving,amount):
        self.personSending = personSending
        self.personReciving = personReciving.split(':')[0]
        self.port =  personReciving.split(':')[1]
        self.amount = amount
        self.status = False
        self.timestamp = time.strftime("%d-%m-%Y-%H-%M-%S.%f")
        self.send_block_chain_manager()
    def send_block_chain_manager(self):
        url = block_chain_manager_url
        transaction_array = [self.timestamp,self.personSending,self.personReciving,self.amount]
        transaction_id =  hashlib.sha256(str(transaction_array)).hexdigest()
        payload = {"timestamp":self.timestamp,"amount":self.amount,"personSending":self.personSending,"personReciving":self.personReciving,"transaction_id":transaction_id,"port":self.port}
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response =  requests.post(url, data=json.dumps(payload), headers=headers)
        print response.content,type(response.content)
        response = json.loads(response.content)
        if int(response["status_code"]) == 200:
            self.status = True
        else:
            self.error = "manager server not found"


class Block:
    def __init__(self,data,previous_block):
        self.previous_block = previous_block
        self.data = data
        self.header = {}
    def create_header(self):
        self.markel_root = calculate_markel_root(self.data)
        self.header = {"markel_root":self.markel_root,"previous_block":self.previous_block}
        self.blockhash = hashlib.sha256(json.dumps(self.header)).hexdigest()
        self.header["blockhash"] = self.blockhash
        return self.header
