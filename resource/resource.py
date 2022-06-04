from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet

import requests
import pandas as pd
import os
import time

MAIN_NETWORK_ID = 1
LISBON_TEST_NETWORK_ID = 2
EXA = 10**18

# parse voterlist from tracker
def getVoterList(PREP_ADDRESS):
    page_count = 0
    voterList = []
    url = f'https://main.tracker.solidwallet.io/v3/iiss/delegate/list?page=1&count=10&prep={PREP_ADDRESS}'
    res = requests.get(url).json()
    page_count = res["totalSize"] // 100 + (res["totalSize"] % 100 != 0)
    print("pagecount = ",page_count)
    print("total voters = ", res["totalSize"])

    for page in range(1, page_count + 1, 1):
        url = f'https://main.tracker.solidwallet.io/v3/iiss/delegate/list?page={page}&count=100&prep={PREP_ADDRESS}'
        data = requests.get(url).json()
        for voter in data["data"]:
            voterDict = {"address": voter["address"], "amount": voter["amount"]}
            voterList.append(voterDict)
    return voterList

# save voters list to csv
def exportVotersList(voterList):
    # remove old file if exist
    if os.path.exists("voters.csv"):
        os.remove("voters.csv")
    df = pd.DataFrame(voterList)
    # saving the dataframe
    df.to_csv('voters.csv')

# calculate total votes and voter share
def getVoterShare(voterList, ICX_DISTRIBUTION_AMOUNT):
    totalVotes = 0
    reward = 0
    voterShareList = []
    for voter in voterList:
        totalVotes += voter["amount"]
    print("totalvotes(ICX) = ",totalVotes)

    for voter in voterList:
        voterShare = voter["amount"]/totalVotes
        reward = voterShare * ICX_DISTRIBUTION_AMOUNT
        voter.update({"share": voterShare, "reward": reward })
        voterShareList.append(voter)
    return voterShareList

# Send icx to recipient address.
def sendTx(recipientAddress, value, wallet, icon_service, network):
    amount = int(value * EXA)
    # Generates an instance of transaction for sending icx.
    # change nid to testnet/mainnet
    transaction = TransactionBuilder()\
        .from_(wallet.get_address())\
        .to(recipientAddress)\
        .value(amount)\
        .step_limit(500000000)\
        .nid(network)\
        .nonce(100)\
        .build()

    # Returns the signed transaction object having a signature
    signed_transaction = SignedTransaction(transaction, wallet)
    print("Sending ", amount/EXA, " ICX to ", recipientAddress)

    # Sends the transaction
    tx_hash = icon_service.send_transaction(signed_transaction)
    print("hash =", tx_hash)

    return tx_hash

# Send icx to recipient address.
def distribute(voter_share_list, wallet, SHOWTXRESULT, icon_service, network):
    distributionResult = []
    for voter in voter_share_list:
        tx_hash = sendTx(voter["address"],voter["reward"], wallet, icon_service, network)
        tx_res = 0


        if SHOWTXRESULT:
            # Waiting 5 seconds for tracker to register transaction
            time.sleep(5)
            # Returns the result of a transaction by transaction hash
            tx_result = icon_service.get_transaction_result(tx_hash)
            print("tx_result [status : 1 on success, 0 on failure]", tx_result["status"])
            tx_res = tx_result["status"]

        voter.update({"hash": tx_hash, "tx_result": tx_res})
        distributionResult.append(voter)
    return distributionResult

