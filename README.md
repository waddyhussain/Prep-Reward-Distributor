# Prep-Reward-Distributor
This scripts gets the voters and bonders of a prep and calculates the percentage of their votes/bonds to distribute 
rewards as per their share.

Twitter: [@bearsurvivor](https://twitter.com/BearSurvivor)

## How to Run Script
**Create virtual environment**

`python3 -m venv venv`

**Activate virtual environment**

Windows: `venv\Scripts\activate`\
Linux: `source venv/bin/activate`


**Install Dependencies**

`pip install -r requirements.txt`

**Run distribution script**

`python3 distribute.py`

## Parameters 

In `config.py` update the following parameters

- `SHOWTXRESULT` = `False` or `True`


- `NETWORK` = `LISBON_TEST_NETWORK_ID` or `MAIN_NETWORK_ID`


- `KEYSTORE_PATH` = Path to keystore file (relative paths will be evaluated from execution directory)


- `PASSWORD` = Password for keystore file


- `PREP_ADDRESS` = Prep address, e.g `"hx43...678"`


Then set the distribution amounts in `distribute.py`

- `VOTERS_DISTRIBUTION_AMOUNT` - amount in ICX to be distributed between voters


- `BONDERS_DISTRIBUTION_AMOUNT` - amount in ICX to be distributed between bonders

If you want to distribute an amount proportional to the distributor wallet's balance, you can use the `balance` 
variable (e.g to distribute 50% of the balance to voters you would do `VOTERS_DISTRIBUTION_AMOUNT = balance * 0.5`)
