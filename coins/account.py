import hashlib
import csv
import time

block_chain_manager_url = "localhost:9000/manager/"

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
    print sub_t
    if len(sub_t) == 1:
       return sub_t[0]
    else:
       return m_tree(sub_t)

def calculate_markel_root(data):
    transactions = []
    for elem in data:
        transactions.append(elem["transaction_id"])
    markel_root = m_tree(transactions)
    print markel_root
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
    def recieve(self,value):
        self.balance = self.balance + value

class Transaction:
    def __init__(self,personSending,personReciving,amount):
        self.csv_file = get_csv_file()
        self.personSending = personSending
        self.personReciving = personReciving.split(':')[0]
        self.port =  personReciving.split(':')[1]
        self.amount = amount
        self.timestamp = time.strftime("%d-%m-%Y-%H-%M-%S.%f")
        self.send_block_chain_manager()
    def send_block_chain_manager(self):
        url = block_chain_manager_url
        transaction_array = [self.timestamp,self.personSending,self.personReciving,self.amount]
        transaction_id =  hashlib.sha256(str(transaction_array)).hexdigest()
        payload = {"timestamp":self.timestamp,"amount":self.amount,"personSending":self.personSending,"personReciving":self.personReciving,"transaction_id":transaction_id,"port":self.port}
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response =  requests.post(url, data=json.dumps(payload), headers=headers)
        if int(response.status_code) == 200:
            self.status = True
        else:
            self.error = "manager server not found"
    def write_to_file(self):
        writer = csv.writer(self.csv_file)
        transaction_array = [self.personSending,self.personReciving,self.amount]
        transaction_id =  hashlib.sha256(str(transaction_array)).hexdigest()
        transaction_array.append(transaction_id)
        writer.writerow(transaction_array)
        self.csv_file.close()


class Block:
    def __init__(self,data,previous_block):
        self.previous_block = previous_block
        self.data = data
    def create_header(self):
        self.markel_root = calculate_markel_root(self.data)
        self.header = {"markel_root":self.markel_root,"previous_block":self.previous_block}
        self.blockhash = hashlib.sha256(json.dumps(header)).hexdigest()
        header["blockhash"] = self.blockhash
        return header


def test_everthing():
    person_1 = account("person_1")
    person_2 = account("person_2")
    person_3 = account("person_3")
    #person_1 (->)gives person_2 5
    amount = 5
    success = person_1.send(amount)
    person_2.recieve(amount)
    if success:
        transaction_1  = transaction(person_1.hexcode,person_2.hexcode,amount)
    #person_2 (->)gives person_3 3
    amount = 3
    success = person_2.send(amount)
    person_3.recieve(amount)
    if success:
        transaction_2  = transaction(person_2.hexcode,person_3.hexcode,amount)
    #block_1 = block(csv_file,'0'*len(person_1.hexcode))
    #block_1.create_header()
 
def get_csv_file():
    date = time.strftime("%d-%m-%Y-%H-%M")
    filename = './data/'+date + '_transaction.csv'
    csv_file = open(filename,"a+r")
    return csv_file

if __name__=="__main__":
    test_everthing()
