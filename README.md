# (unofficial) Python Client for Sanctum API

This library is a simple Python client for the Sanctum API. It's aimed to 
help automate your LSTs management.


## Disclaimer

Be aware that this client directly communicates with Sanctum. Be sure of your
script before doing any financial operations. Moreover, there is no guarantee
about the reliability of this client. I encourage you to tests your scripts
before using them on the mainnet.

The developer of this client is not responsible for any errors or issues that
may occur when using this client. Use at your own risk.

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

## Documenation

A [full documentation](https://sanctumpy.thewise.trade/) is available (coming soon).


## Contributions

Any contribution is welcome, please open your PR for additions and report bug
through Github issues.

## About

This client is developed by [thewise.trade](https://thewise.trade).

If you like this client, you can tip me at: thewisetrade.sol or buy 
[the logo NFT](https://exchange.art/editions/9rukfGYfTxpmiRFrGvhSSCASsqhgsWGundBHNQB2vKPy).
