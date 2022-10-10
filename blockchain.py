import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
        # Create the genesis block
        self.new_block(previous_hash=1, proof = 100)

    """
    Creates a new Block and adds it to the chain
    :param proof: <int> The proof value
    :param previous: (Optional) <str> Hash of previous Block
    :return: <dict> New Block
    """
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Clear the current transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    """
    Adds a new transaction to the list of transactions
    :param sender: <str> Address of Sender
    :param recipient: <str> Address of Recipient
    :param amount: <int> Amount
    :return: <int> Index of Block that holds transaction
    """
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1
    
    """
    Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains leading
        4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
    :param last_proof: <int>
    :return: <int>
    """
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    """
    Validates the Proof: Does hash(last_proof, proof) contain 4
    leading zeroes?
    :param last_proof: <int> Previous Proof
    :param proof: <int> Current Proof
    :return: <bool> True if correct, False if not.
    """
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    """
    Creates a SHA-256 hash of a Block
    :param block: <dict> Block
    :return: <str>
    """
    @staticmethod
    def hash(block):
        # Must make sure dictionary is ordered or hashes will be inconsistent
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
    
    
    @property
    # Returns last Block in chain
    def last_block(self):
        return self.chain[-1]


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate Beckmancoin Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # Run proof of work to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Must receive a reward for finding POW
    # Sender is "0" to show that this node has mined a new coin

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge new Block by adding it to chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "Missing values", 400
    
    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)