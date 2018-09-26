# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 00:01:12 2018

@author: Ahmed Hassanein
"""

# importing the libs

import datetime
import hashlib
import json
from flask import Flask,jsonify

# part 1 Building a Blockchain

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1,prev='0')

    def create_block(self,proof,prev):
        block = {'index':len(self.chain)+1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':prev}
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,prev_proof):
        new_proof =1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 -prev_proof**2).encode()).hexdigest()
            if hash_operation[:4]== '0000':
                check_proof =True
            else:
                new_proof +=1
        return new_proof
    
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        prev_block = chain[0]
        block_index=1
        while block_index<len(chain):
            block = chain[block_index]
            if self.hash(prev_block) != block['previous_hash']:
                return False
            prev_proof= prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 -prev_proof**2).encode()).hexdigest()
            if hash_operation[:4]!= '0000':
                return False
            prev_block = block
            block_index += 1
        return True
    
    
# Part 2 - mining our blockchain

# create a web app
app =Flask(__name__)

    
    
# create a blockchain
blockchain = Blockchain()

# mine the blockchain
@app.route('/mine_block',methods=['GET'])
def mine_block():
    prev_block = blockchain.get_previous_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash= blockchain.hash(prev_block)
    block = blockchain.create_block(proof,prev_hash)
    response ={'message':'Congratulations, You just mined a block',
               'index':block['index'],
               'timestamp':block['timestamp'],
               'proof':block['proof'],
               'prev_hash':block['previous_hash']}
    return jsonify(response),200


    
# get chain
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response),200

# running the app
app.run(host ='0.0.0.0',port=5000)
    
    
    
    

        
            
            
            
