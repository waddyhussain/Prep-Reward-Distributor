from config import MAIN_NETWORK_ID, LISBON_TEST_NETWORK_ID, NETWORK, SHOWTXRESULT, KEYSTORE_PATH, PASSWORD, PREP_ADDRESS, CLAIM_ISCORE
import resource

from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet


if NETWORK == LISBON_TEST_NETWORK_ID:
    icon_service = IconService(HTTPProvider("https://lisbon.net.solidwallet.io", 3))
elif NETWORK == MAIN_NETWORK_ID:
    icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))

# Load wallet
wallet = KeyWallet.load(KEYSTORE_PATH, PASSWORD)
print("Distributor address:", wallet.get_address()) # Returns an address

if CLAIM_ISCORE:
    resource.claimIScore(wallet, icon_service, NETWORK)

# Get balance
balance = icon_service.get_balance(wallet.get_address()) / 10**18
print(f"Balance: {balance} ICX")

# 1. Enter ICX amount for distribution between voters (set as 0 if you don't want to distribute to voters)
# Distributor wallet must have the distribution amount in ICX
VOTERS_DISTRIBUTION_AMOUNT = 50

if VOTERS_DISTRIBUTION_AMOUNT:
    # Scrap voter list
    if NETWORK == LISBON_TEST_NETWORK_ID:
        # This is dummy list for testing change addresses
        voter_list=[{"address": "hxcb3204...8db2a7f1", "amount": 100},{"address":"hx24598bf...66f57990c", "amount": 50},{"address": "hx02dd...1d1", "amount": 25},{"address": "hxd2495...c1ef", "amount": 25}]
    elif NETWORK == MAIN_NETWORK_ID:
        voter_list= resource.getVoterList(PREP_ADDRESS)

    # Calculate voter share
    voter_share_list = resource.getShare(voter_list, VOTERS_DISTRIBUTION_AMOUNT)

    # Distribute the rewards
    distribution_result = resource.distribute(voter_share_list, wallet, SHOWTXRESULT, icon_service, NETWORK)

    # Export voter list with results voters.csv
    resource.exportList(distribution_result, "voters.csv")

# 2. Enter ICX amount for distribution between bonders (set as 0 if you don't want to distribute to bonders)
# Distributor wallet must have the distribution amount in ICX
BONDERS_DISTRIBUTION_AMOUNT = 50

if BONDERS_DISTRIBUTION_AMOUNT:
    # Scrap bonder list
    if NETWORK == LISBON_TEST_NETWORK_ID:
        # This is dummy list for testing change addresses
        bonder_list=[{"address": "hxcb3204...8db2a7f1", "amount": 100},{"address":"hx24598bf...66f57990c", "amount": 50},{"address": "hx02dd...1d1", "amount": 25},{"address": "hxd2495...c1ef", "amount": 25}]
    elif NETWORK == MAIN_NETWORK_ID:
        bonder_list= resource.getBonderList(icon_service, wallet, PREP_ADDRESS)

    # Calculate bonder share
    bonder_share_list = resource.getShare(bonder_list, BONDERS_DISTRIBUTION_AMOUNT)

    # Distribute the rewards
    distribution_result = resource.distribute(bonder_share_list, wallet, SHOWTXRESULT, icon_service, NETWORK)

    # Export voter list with results bonders.csv
    resource.exportList(distribution_result, "bonders.csv")
