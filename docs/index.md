# (unofficial) Python Client for Sanctum

This library is a simple Python client for the Sanctum API. It's aimed is 
to make your Sanctum automation simpler.


## Disclaimer

Be aware that this client directly communicates with Sanctum. Be sure of your
script before doing any financial operations. Moreover, there is no guarantee
about the reliability of this client. I encourage you to tests your scripts
with cheap transactions first. 

The developer of this client is not responsible for any errors or issues that
may occur when using this SDK. Use at your own risk.


## Install

Install the library with:

```
pip install git+https://github.com/defilogist/sanctum-py
```

## Usage example

``` python
import os
from sanctumpy import SanctumClient

client = SanctumClient(
    os.getenv("TENSOR_API_KEY"),
    os.getenv("WALLET_PRIVATE_KEY"), # optional
    "mainnet-beta" # optional
)

inf_infos = client.get_infinity_infos()
jupsol_apy = client.get_lst_apy("JupSOL")
jupsol_value = client.get_lst_sol_value("JupSOL")
jupsol_tvl = client.get_lst_tvl("JupSOL")
jupsol_infos = client.get_lst_infos("JupSOL")
jupsol_price = client.get_price("jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v")
metadata = client.get_metadata("jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v")
quote = client.get_quote("jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v", "BonK1YhkXEGLZzwtcvRTip3gAL9nCeQD7ppZBLXhtTs", 1)
```


## Functions available

All functions available are listed in the 
[specifications]("https://sanctumpy.thewise.trade/specifications") section.

## About

This client is developed by [defilogist (thewise.trade)](https://thewise.trade).

You can tip us at thewisetrade.sol or by [buying our NFT](https://exchange.art/editions/9rukfGYfTxpmiRFrGvhSSCASsqhgsWGundBHNQB2vKPy)
