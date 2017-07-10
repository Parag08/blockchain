from flask import Flask, render_template, request, url_for
import account
import random
import threading
import time
import sys
import requests, json
import os
import datetime

app = Flask(__name__)

transactions_array = []
previous_block = '0'*64
previous_block_num = 0

data_dir = "./data/"


def intialise():
    global previous_block
    global previous_block_num
    most_recent = 0
    most_recent_file = ''
    for blk_file in os.listdir(data_dir):
        if blk_file.endswith(".blk"):
            try:
                if most_recent < int(blk_file[0:-4]):
                    most_recent = int(blk_file[0:-4])
                    most_recent_file = os.path.join(data_dir, blk_file)
            except Exception as exp:
                print exp
    previous_block_num = most_recent
    if most_recent != 0:
        with open(most_recent_file) as data_file:
            data = json.load(data_file)
            previous_block = data["header"]["blockhash"]
    print previous_block, previous_block_num


@app.route("/manager/",methods=['POST'])
def transactions():
    url = "http://127.0.0.1:"+request.json['port']+"/"+request.json["personReciving"]+"/"
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    payload = {"timestamp":datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S.%f"),"amount":request.json["amount"]}
    response =  requests.post(url, data=json.dumps(payload), headers=headers)
    if int(response.status_code) == 200:
        transactions_array.append(request.json)
        if len(transactions_array) == 10:
            global previous_block
            global previous_block_num
            block = account.Block(transactions_array,previous_block)
            header = block.create_header()
            previous_block = header["blockhash"]
            print "block HASHED:" + previous_block
            data = {}
            data["header"] = header
            data["transactions"] = transactions_array
            previous_block_num = previous_block_num + 1
            blk_file = data_dir + str(previous_block_num) + '.blk'
            with open(blk_file, 'w') as outfile:
                    json.dump(data, outfile)
    return json.dumps({"status_code":response.status_code})


if __name__ == "__main__":
    intialise()
    app.run(
            port=9000
    )
