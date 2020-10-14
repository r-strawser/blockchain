# Module 2 - Create a Cryptocurrency

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/
# requests==2.18.4: pip install requests==2.18.4

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    # returns: the index of the block that will receive the transactions
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        # since last block is a fixed block and cannot receive transactions,
        # use the next block (+1) which can
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    # adds the node containing the specified address to the set of nodes
    def add_node(self, address):
        # parse the address of the node
        parsed_url = urlparse(address)
        
        # add node to network --> netloc is url and port 5000 we are using
        # example: http://127.0.0.1.5000/ --> netloc --> 127.0.0.1.5000
        self.nodes.add(parsed_url.netloc)
        
        
    
    # replaces the chain on the node which is being applied
    # only takes in 'self' because each node will take in a specific version
    # of the blockchain
    # max_length is the length of the longest_chain
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        # for all nodes in network, find the largest chain
        # uses requests library to seek our specific response of get_chain
        # and get the length of the chain in the specific node
        # nodes are differentiated by their port (i.e. 127.0.0.1:5000, 5001, 5002, 5746)
        # node could =  '127.0.0.1:5000 or whatever port it is
        for nodes in network:
            response = requests.get(f'http://{node}/get_chain')
            # if found node and return success code, get chain data and check for longer chain
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # if length is greater than max_length and is valid, replace current chain as updated chain
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        # if longest_chain is not None, that means chain was replaced, we can place the chain and return true
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port: 5000
# replaces dashes with nothing
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Ryan', amount = 1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Part 3 - Decentralizing our Blockchain

# Running the app
app.run(host = '0.0.0.0', port = 5000)
