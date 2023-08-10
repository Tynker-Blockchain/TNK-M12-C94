# SA1: Create a mining pool

from flask import Flask, render_template, request
import os
from time import time
from blockchain import BlockChain, Block
from conversion import getGasPrices

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

chain = BlockChain()
currentBlock = None
failedBlocks = []

@app.route("/", methods= ["GET", "POST"])
def home():
    global blockData, currentBlock, chain, failedBlocks
     
    allPrices = getGasPrices()
    
    if request.method == "GET":
        return render_template('index.html', allPrices = allPrices)
    else:
        sender = request.form.get("sender")
        receiver = request.form.get("receiver")
        artId = request.form.get("artId")
        amount = request.form.get("amount")
        mode = request.form.get("mode")

        gasPrices, gweiPrices, etherPrices, dollarPrices = allPrices
        
        gasPriceGwei = gweiPrices[mode]
        gasPriceEther = etherPrices[mode]
        transactionFeeEther = etherPrices[mode] * 21000
        transactionFeeDollar = dollarPrices[mode] * 21000
        
        transaction = { 
                "sender": sender, 
                "receiver": receiver, 
                "amount": amount,
                "artId": artId,            
                "gasPriceGwei" : gasPriceGwei,
                "gasPriceEther" : gasPriceEther, 
                "transactionFeeEther" : transactionFeeEther,
                "transactionfeeDollar" : transactionFeeDollar
            }  

        # Adding transaction to mining pool
        chain.addToMiningPool(transaction)

        # Comment down all the code
        # index = chain.length()
        # if index==0:
        #     index = 1
        # blockData = {
        #         'index': index,
        #         'timestamp': time(),
        #         'previousHash': "No Previous Hash.",
        # }   
        
        # if currentBlock == None:
        #     currentBlock = Block(
        #                     blockData["index"], 
        #                     blockData["timestamp"], 
        #                     blockData["previousHash"])
        
        # status = currentBlock.addTransaction(transaction)
        
        # if status == "Ready":
        #     isBlockAdded = chain.addBlock(currentBlock) 
        #     if(isBlockAdded):  
        #         isValid = chain.validateBlock(currentBlock)
        #         currentBlock.isValid = isValid
        #         currentBlock = None
        #     else:
        #         currentBlock.index = "Failed"+ str(currentBlock.index) + str(len(failedBlocks))
        #         failedBlocks.append(currentBlock)
        #         currentBlock = None
   
    return render_template('index.html', blockChain = chain, allPrices = allPrices)


@app.route("/blockchain", methods= ["GET", "POST"])
def show():
    global chain, currentBlock, failedBlocks

    currentBlockLength  = 0
    if currentBlock:
        currentBlockLength = len(currentBlock.transactions)
    
    return render_template('blockchain.html', blockChain = chain.chain, currentBlockLength = currentBlockLength, failedBlocks= failedBlocks)
    

@app.route("/miningPool", methods= ["GET", "POST"])
def miningPool():
    global chain
    # Return the pendingTransactions from chain as pendingTransactions
    return render_template('miningPool.html', pendingTransactions = chain.pendingTransactions)

if __name__ == '__main__':
    app.run(debug = True, port=4001)