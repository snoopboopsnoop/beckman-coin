import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
        # Create the genesis block
        self.new_blocK(previous_hash=1, proof = 100)

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
    
    @staticmethod
    """
    Creates a SHA-256 hash of a Block
    :param block: <dict> Block
    :return: <str>
    """
    def hash(block):
        # Must make sure dictionary is ordered or hashes will be inconsistent
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
    
    @property
    # Returns last Block in chain
    def last_block(self):
        pass