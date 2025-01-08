#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime
import json


class Block:
    """Represents a block in the blockchain."""

    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        """
        Initialize a new block with :
        - index : the index of the block in the blockchain
        - transactions : a list of transactions
        - previous_hash : the hash of the previous block
        - timestamp : the timestamp of the block creation
        - nonce : Value of the proof of work
        """
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce                      # Using nonce for proof of work
        self.hash = self.generate_hash()        # Hash of the block

    def generate_hash(self):
        """
        Calculates the hash of the block based on its contents.
        Combines index, transactions, previous_hash, timestamp and nonce into a JSON string 
        and generates a SHA-256 hash.
        """
        block_string = (str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce))
        return hashlib.sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, difficulty):
        """
        Performs a proof of work by finding a hash with a certain number of zeros.
        Increments the nonce until the hash starts with 'difficulty' zeros.
        """
        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.generate_hash()

            
class Transaction:
    """Represents a transaction in the blockchain."""

    def __init__(self, sender, receiver, amount):
        """
        Initialize a new transaction with:
        - sender: The identifier of the sender.
        - recipient: The identifier of the recipient.
        - amount: The amount being transferred.
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_json(self):
        """
        Serializes the transaction into a JSON-compatible dictionary.
        """
        return {"sender": self.sender,
                "receiver": self.receiver,
                "amount": self.amount
                }
    
    def is_valid(self):
        """
        Validates the transaction.
        Ensures that all fields are properly filled and the amount is positive.
        """
        if not self.sender or not self.receiver: 
            return False                        # Sender and receiver must be filled
        if self.amount <= 0:
            return False                        # Amount must be positive 
        return 

    
class Blockchain:
    """
    Represents a chain of blocks.
    """

    def __init__(self):
        """
        Initializes the blockchain with a genesis block and a list to store blocks.
        """
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        """
        Creates the first block in the blockchain, known as the genesis block.
        """
        return Block(0, datetime.now().strftime("%d/%m/%Y %H:%M:%S %f"), [], "0")
    
    def add_block(self, new_block, difficulty):
        """
        Adds a new block to the blockchain after solving the proof of work.
        """
        new_block.previous_hash = self.chain[-1].hash
        new_block.proof_of_work(difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Validates the entire blockchain.
        Ensures that each block's hash and linkage to the previous block is correct.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is correct
            if current_block.hash != current_block.generate_hash():
                return False

            # Check if the current block's previous hash matches the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def display_chain(self):
        """
        Displays the blockchain in a readable format.
        """
        for block in self.chain:
            print(json.dumps({
                "index": block.index,
                "timestamp": block.timestamp,
                "transactions": block.transactions,
                "hash": block.hash,
                "previous_hash": block.previous_hash,
                "nonce": block.nonce
            }, indent=4))

    def resolve_conflicts(self, other_chain):
        """
        Resolves conflicts by replacing the chain with the longest valid chain if necessary.
        """
        if len(other_chain) > len(self.chain) and self.is_valid_chain(other_chain):
            self.chain = other_chain

    def is_valid_chain(self, chain):
        """
        Validates an external chain.
        """
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            # Check if the current block's hash is correct
            if current_block.hash != current_block.generate_hash():
                return False

            # Check if the current block's previous hash matches the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                return False

        return True