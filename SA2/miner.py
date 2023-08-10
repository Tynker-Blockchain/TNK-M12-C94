from time import time
from blockchain import Block

class Miner():
    def __init__(self, address):
        self.address= address
        self.walletBalance = 0    
   
    # Define createBlock method that takes index of the block and transactions list
    def createBlock(self, index, transactions):
        # Check if transactions length greater then 3
        if(len(transactions) >=3 ):
            # Get first three transactions in transactions variable
            transactions = transactions[:3]

            # Take this code from commeted code in app.py same done in previous classes
            if index==0:
                index = 1
            blockData = {
                    'index': index,
                    'timestamp': time(),
                    'previousHash': "No Previous Hash.",
            }    

            currentBlock = Block(
                                blockData["index"], 
                                blockData["timestamp"], 
                                blockData["previousHash"])

            # Add transactions to currentBlock.transactions               
            currentBlock.transactions = transactions

            # Return the current block
            return currentBlock
        # Return false if transactions are less then 3
        return False
