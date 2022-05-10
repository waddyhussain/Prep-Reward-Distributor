# Prep-Reward-Distributor
This scripts scrape the voters of a prep from tracker and calculates the percentage of their votes to distribute rewards as per their share.

Twitter: [@bearsurvivor](https://twitter.com/BearSurvivor)

## How to Run Script
**Create virtual environment**

`virtualenv env`

**activatre virtual environment**

`env\Scripts\activate`

**Install Dependencies**

`pip install -r requirements.txt`

**Run distribution script**

`distribute.py`

## Parameters 

In distribute.py update the following parameters

**Showing Tx result in Voters.csv**

[status : 1 on true, 0 on false]

`SHOWTXRESULT = 0`

**Selecting network**

`network = LISBON_TEST_NETWORK_ID`

or

`network = MAIN_NETWORK_ID`

**Adding wallet**

`wallet = KeyWallet.load("./keystoreFileName", "Password")`

**Adding prep address**

`PREP_ADDRESS = "hx43...678"`

**Adding distribution amount**

`ICX_DISTRIBUTION_AMOUNT = 100`
