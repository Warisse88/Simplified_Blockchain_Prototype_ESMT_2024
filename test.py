#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from datetime import datetime
from prototype import Block, Transaction, Blockchain
import json

# Test 1
def test_hash_generation():
    '''Validate that each block generates a unique hash based on its content.'''
    transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 50},
        {"sender": "Charlie", "receiver": "David", "amount": 25}
    ]
    block = Block(index=1, transactions=transactions, previous_hash="0000abcdef")
    generated_hash = block.generate_hash()

    assert generated_hash == block.hash, "The generated hash should match the block's stored hash."

# Test 2
def test_hash_change_on_modification():
    '''Modify a block's content and verify that the hash changes.'''
    transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 50},
        {"sender": "Charlie", "receiver": "David", "amount": 25}
    ]
    block = Block(index=1, transactions=transactions, previous_hash="0000abcdef")

    # Capture the original hash
    original_hash = block.hash

    # Modify the transactions
    block.transactions.append({"sender": "Eve", "receiver": "Mallory", "amount": 100})
    modified_hash = block.generate_hash()

    assert original_hash != modified_hash, "The hash should change after modifying the block's content."

# Test 3
def test_transaction_valid():
    '''Validate a transaction with a positive amount.'''
    
    transaction = Transaction("Boubs", "Amina", 500)
    assert transaction.is_valid() == True, "Valid transaction failed validation."

# Test 4
def test_transaction_invalid_negative_amount():
    '''Validate a transaction with a negative amount.'''
    transaction = Transaction("Sonia", "Felix", -100)
    assert transaction.is_valid() == False, "Transaction with negative amount passed validation."

# Test 5:
def test_transaction_serialization():
    '''Verify the JSON serialization of a transaction.'''
    transaction = Transaction(sender="Alice", receiver="Bob", amount=50)
    serialized = transaction.to_json()

    expected_serialized = {"sender": "Alice", 
                           "receiver": "Bob", 
                           "amount": 50
                           }

    assert serialized == expected_serialized, "The serialized transaction should match the expected JSON format."

# Test 6
def test_proof_of_work():
    '''Verify that the proof of work generates a hash with the correct number of leading zeros.'''
    transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 50}
    ]
    block = Block(index=1, transactions=transactions, previous_hash="0000abcdef")

    difficulty = 3
    block.proof_of_work(difficulty)

    assert block.hash.startswith("0" * difficulty), "The hash should start with the correct number of leading zeros."


# Test 7
def test_proof_of_work_timing_with_datetime():
    '''Calculate the time taken to solve the proof of work at different difficulties.'''
    transactions = [
        {"sender": "Alice", "receiver": "Bob", "amount": 50}
    ]
    difficulties = [0, 1, 2, 3, 4, 5, 6]

    for difficulty in difficulties:
        block = Block(index=1, transactions=transactions, previous_hash="0000abcdef")
        start_time = datetime.now()
        block.proof_of_work(difficulty)
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()

        assert block.hash.startswith("0" * difficulty), "The hash should start with the correct number of leading zeros."

# Test 8:
def test_blockchain_genesis_block():
    '''Validate genesis block'''
    blockchain = Blockchain()
    assert blockchain.is_chain_valid() == True, "Blockchain with genesis block should be valid."

# Test 9:
def test_add_block_and_validate():
    '''Add a new block and validate the chain'''
    blockchain = Blockchain()
    transaction = Transaction("Alice", "Bob", 100)
    new_block = Block(index=1, 
                      timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S %f"), 
                      transactions=[transaction.to_json()], 
                      previous_hash="")
    blockchain.add_block(new_block, difficulty=2)
    assert blockchain.is_chain_valid() == True, "Blockchain should be valid after adding a block."

# Test 10:
def test_tampered_block():
    '''Tamper with a block and validate the chain'''
    blockchain = Blockchain()
    transaction = Transaction("Alice", "Bob", 100)
    new_block = Block(index=1, 
                      timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S %f"), 
                      transactions=[transaction.to_json()], 
                      previous_hash="")
    blockchain.add_block(new_block, difficulty=2)
    blockchain.chain[1].transactions.append({"sender": "Eve", "receiver": "Mallory", "amount": 200})
    assert blockchain.is_chain_valid() == False, "Tampered blockchain should be invalid."

# Test 11:
def test_resolve_conflicts():
    '''Resolve conflicts by replacing the chain with a longer valid chain'''
    blockchain = Blockchain()
    other_chain = Blockchain()

    # Add a block to the original chain
    transaction = Transaction("Alice", "Bob", 100)
    new_block = Block(index=1,
                      timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S %f"), 
                      transactions=[transaction.to_json()], 
                      previous_hash="")
    
    blockchain.add_block(new_block, difficulty=2)

    # Add two blocks to the other chain
    other_block = Block(index=1, 
                        timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S %f"),
                        transactions=[{"sender": "John", "receiver": "Jane", "amount": 50}], 
                        previous_hash="")
    other_chain.add_block(other_block, difficulty=2)

    other_block_2 = Block(index=2,
                          timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S %f"),
                          transactions=[{"sender": "Marie", "receiver": "Ange", "amount": 90}], 
                          previous_hash="")
    other_chain.add_block(other_block_2, difficulty=4)

    # Resolve conflicts
    # Original chain before resolving conflicts
    #print("Original Chain Length:", len(blockchain.chain))

    blockchain.resolve_conflicts(other_chain.chain)

    # Original chain after resolving conflicts
    #print("New Chain Length:", len(blockchain.chain))

    assert len(blockchain.chain) == len(other_chain.chain), "Blockchain should adopt the longer valid chain."

