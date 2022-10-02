import hashlib
import json

from time import time
from uuid import uuid4

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
        guess_has = hashlib.sha256(guess).hexdigest()
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
        pass