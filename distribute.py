from resource import resource
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet

MAIN_NETWORK_ID = 1
LISBON_TEST_NETWORK_ID = 2

#1 First select network
#select network here
network = LISBON_TEST_NETWORK_ID

#2 Select if you want tx result status //this adds extra delay
#[status : 1 on true, 0 on false]
SHOWTXRESULT = 0

if network == LISBON_TEST_NETWORK_ID:
    icon_service = IconService(HTTPProvider("https://lisbon.net.solidwallet.io", 3))
elif network == MAIN_NETWORK_ID:
    icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))

#3 Select wallet here add keystore file should be in the same directory
# Loads a Distributor Wallet from a keystore file
wallet = KeyWallet.load("./keystoreFileName", "Password")
print("Distributor address: ", wallet.get_address()) # Returns an address

#4 Enter prep address here
PREP_ADDRESS = "hx437...678"

# 5 Select if you want to claim I-Score for PRep
# [True or False]
CLAIM_ISCORE = False
if CLAIM_ISCORE:
    resource.claimIScore(wallet, icon_service, network)

# Get balance
balance = icon_service.get_balance(wallet.get_address())
print("balance: ", balance)

#5 Enter ICX amount for distribution
# distributor Wallet must have the distribution amount in ICX
ICX_DISTRIBUTION_AMOUNT = 100

# scrap voter list
if network == LISBON_TEST_NETWORK_ID:
    # this is dummy list for testing change addresses
    voter_list=[{"address": "hxcb3204...8db2a7f1", "amount": 100},{"address":"hx24598bf...66f57990c", "amount": 50},{"address": "hx02dd...1d1", "amount": 25},{"address": "hxd2495...c1ef", "amount": 25}]
elif network == MAIN_NETWORK_ID:
    voter_list= resource.getVoterList(PREP_ADDRESS)

# calculate voter share
voter_share_list = resource.getVoterShare(voter_list, ICX_DISTRIBUTION_AMOUNT)

# distribute the rewards
distribution_result = resource.distribute(voter_share_list, wallet, SHOWTXRESULT, icon_service, network)

# export voter list with results voters.csv
resource.exportVotersList(distribution_result)

