from flask import Flask, render_template, request, url_for
import account
import random
import threading
import time
import sys
import requests, json



my_account = account.Account('person_1')

app = Flask(__name__)

@app.route("/"+my_account.hexcode+"/",methods=['GET'])
def account_balance():
    return str(my_account.balance)

@app.route("/"+my_account.hexcode+"/",methods=['POST'])
def recieved():
    amount = int(request.json['amount'])
    print "you received:" + str(amount)
    my_account.recieve(amount)
    return "thanks for the coins"

'''
@app.route("/manager/",methods=['POST'])
def transactions():
    request.json
'''

def runFlaskserver():
    app.run(
            port=my_account.port
    )

if __name__ == "__main__":
    thread = threading.Thread(target=runFlaskserver)
    thread.daemon = True
    thread.start()
    register_to_network()
    while True:
        input_string = raw_input("What do you want to do(send/exit/show):")
        if input_string == "send":
            account_id = raw_input("accountid(with port ex:- abc:1234):")
            amount = int(raw_input("amount:"))
            success = my_account.send(amount)
            if success:
                '''
                url = "http://127.0.0.1:"+account_id.split(':')[1]+"/"+account_id.split(':')[0]+"/"
                payload = {"timestamp":time.strftime("%d-%m-%Y-%H-%M-%S.%f"),"amount":amount}
                headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                r = requests.post(url, data=json.dumps(payload), headers=headers)
                if int(r.status_code)==200:
                    True
                '''
                transaction = account.Transaction(my_account.hexcode,account_id,amount)
                if transaction.status = False:
                    print transaction.error
                    my_account.recieve(amount)
            else:
                print "you dont have coins in your account:"+str(my_account.balance)
        elif input_string == "show":
            print "account_id:"+my_account.hexcode
            print "balance:"+str(my_account.balance)
        elif input_string == "exit":
            sys.exit(0)
