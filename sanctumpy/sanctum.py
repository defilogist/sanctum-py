import os
import requests

from .solana import (
    create_client,
    from_solami,
    to_solami,
    get_keypair_from_base58_secret_key,
    run_solana_transaction,
    run_solana_versioned_transaction
)

from .exceptions import (
    TransactionFailedException,
    NoJSONException,
    WrongAPIKeyException,
)


class SanctumClient:

    def __init__(
        self,
        api_key,
        private_key=None,
        network="devnet",
    ):
        """
        The constructor sets up the client. It allows you to set your Sanctum
        Trade API key, your wallet private key to perform operations and the
        Solana network where transactions are set.

        Args:
            api_key (str): The Sanctum Trade API authentication key.
            private_key (str): Your wallet private key.
            network (str): The Solana network to use.
        """
        self.init_client(api_key)
        if private_key is not None and private_key != "":
            self.init_solana_client(private_key, network)

    def init_client(self, api_key: str):
        """
        Initialize the Sanctum Trade client and the `requests` session.

        Arguments:
            api_key (str): The Sanctum Trade API authentication key.
        """
        self.session = requests.session()
        self.api_key = api_key
        self.session.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'sanctumpy 0.1.0'
        }

    def init_solana_client(self, private_key, network):
        """
        Initialize the Solana client.

        Arguments:
            private_key (str): The private key of the wallet.
            network (str): The Solana network to use.

        Returns:
            The solana client object.
        """
        self.keypair = None
        if private_key is not None:
            self.keypair = get_keypair_from_base58_secret_key(private_key)
        url = f"https://api.{network}.solana.com"
        if network.startswith("http"):
            url = network
        self.solana_client = create_client(url)
        return self.solana_client

    def get(self, path, data=None, params=None, extra=False):
        """
        Send a query to the Sanctum Trade API.

        Arguments:
            path (str): The path to send the request to.
            params (dict): The parameters to add to the query.
            extra (bool): Whether to use the extra API.
        """
        host = "sanctum-s-api.fly.dev"
        if extra:
            host = "sanctum-extra-api.ngrok.dev"
        path = f"https://{host}{path}"

        if params is not None:
            path += "?" + "&".join([f"{key}={value}" for key, value in params.items()])

        resp = self.session.get(path)

        try:
            DEBUG = os.getenv("DEBUG", "false")
            if DEBUG == "true":
                print(resp.text)
            try:
                result = resp.json()
            except requests.exceptions.JSONDecodeError:
                raise NoJSONException(resp.text)
            return result
        except requests.exceptions.JSONDecodeError:
            if resp.status_code == 403:
                raise WrongAPIKeyException("Invalid API Key")
            else:
                raise

    def post(self, path, data=None):
        """
        Send a POST request to the Sanctum Trade API.

        Arguments:
            path (str): The path to send the request to.
            data (dict): The data to send to the path.
        """
        host = "sanctum-s-api.fly.dev"
        path = f"https://{host}{path}"
        resp = self.session.post(path, json=data)

        try:
            DEBUG = os.getenv("DEBUG", "false")
            if DEBUG == "true":
                print(resp.text)
            try:
                result = resp.json()
            except requests.exceptions.JSONDecodeError:
                raise NoJSONException(resp.text)
            return result
        except requests.exceptions.JSONDecodeError:
            if resp.status_code == 403:
                raise WrongAPIKeyException("Invalid API Key")
            else:
                raise

    def run_transaction(self, transaction):
        """
        Execute the transaction to the Solana network.

        Arguments:
            transaction (str): The transaction to execute.
        """
        res = run_solana_versioned_transaction(
            self.solana_client,
            self.keypair,
            transaction
        )
        return res

    def check_errors(self, data):
        if len(data["errs"].keys()) > 0:
            raise Exception(data["errs"])
        return data

    def get_infinity_infos(self):
        """
        Retrieve the main information about the INF token.

        Returns:
            (dict): Sanctum Infinity information.
        """

        return self.get(f"/v1/infinity/allocation/current", {}, extra=True)

    def get_lst_apy(self, lst, epochs=None, latest=True):
        """
        Retrieve APY inception data for specified tokens.

        Arguments:
            lst (str): The LST token symbol or address.

        Returns:
            (float): APY inception data for the specified tokens.
        """
        params = {"lst": lst}
        if epochs is not None:
            params["epochs"] = epochs
        data = None
        if latest:
            data = self.get("/v1/apy/latest", params=params, extra=True)
        elif epochs is not None:
            data = self.get("/v1/apy/epochs", params=params, extra=True)
        else:
            data = self.get("/v1/apy/inception", params=params, extra=True)

        data = self.check_errors(data)
        return round(data["apys"][lst] * 100, 2)

    def get_lst_sol_value(self, lst):
        """
        Retrieve the SOL value of the specified LST.

        Arguments:
            lst (str): The LST token symbol or address.

        Returns:
            (float): The SOL value of the specified LST.
        """
        params = {"lst": lst}
        data = self.get("/v1/sol-value/current", params=params, extra=True)
        data = self.check_errors(data)
        return from_solami(data["solValues"][lst])

    def get_lst_tvl(self, lst):
        """
        Retrieve the TVL of the specified LST.

        Arguments:
            lst (str): The LST token symbol or address.

        Returns:
            (float): The TVL of the specified LST.
        """
        params = {"lst": lst}
        data = self.get("/v1/tvl/current", params=params, extra=True)
        data = self.check_errors(data)
        return round(from_solami(data["tvls"][lst]), 2)

    def get_lst_infos(self, lst):
        """
        Retrieve the information of the specified LST.

        Arguments:
            lst (str): The LST token symbol or address.

        Returns:
            (dict): The information of the specified LST (apy, sol_value, tvl).
        """
        apy = self.get_lst_apy(lst)
        sol_value = self.get_lst_sol_value(lst)
        tvl = self.get_lst_tvl(lst)
        return {"apy": apy, "sol_value": sol_value, "tvl": tvl}

    def get_price(self, lst_mint):
        """
        Retrieve the price of the specified LST.

        Arguments:
            lst_mint (str): The LST token mint.
        """
        params = {"input": lst_mint}
        data = self.get(f"/v1/price", params=params)
        return from_solami(data["prices"][0]["amount"])

    def get_metadata(self, lst_mint):
        """
        Retrieve the metadata of the specified LST.

        Arguments:
            lst_mint (str): The LST token mint.
        """
        data = self.get(f"/v1/metadata/{lst_mint}")
        return data

    def get_quote(self, from_token, to_token, amount, mode="ExactIn", swap_src=None):
        """
        Retrieve the quote for the specified token.

        Arguments:
            from_token (str): The token to sell.
            to_token (str): The token to buy.
            amount (float): The amount to sell.
        """
        if mode not in ["ExactIn", "ExactOut"]:
            raise Exception("Invalid mode")
        if swap_src is not None and swap_src not in ["Spool", "Stakedex", "Jup"]:
            raise Exception("Invalid swap source")

        params = {
            "input": from_token,
            "outputLstMint": to_token,
            "amount": to_solami(amount),
            "mode": mode
        }
        if swap_src is not None:
            params["swapSrc"] = swap_src
        data = self.get("/v1/swap/quote", params=params)
        return data

    def add_liquidity(self, amount, lst_mint="So11111111111111111111111111111111111111112"):
        """
        Add liquidity to the specified LST.

        Arguments:
            lst_mint (str): The LST token mint.
            amount (float): The amount to add.
        """
        params = {
            "amount": str(to_solami(amount)),
            "dstLpAcc": None,
            "lstMint": lst_mint,
            "priorityFee": {
                "Auto": {
                    "max_unit_price_micro_lamports": 3000,
                    "unit_limit": 300000
                }
            },
            "quotedAmount": str(to_solami(amount)),
            "signer": str(self.keypair.pubkey()),
            "srcLstAcc": None
        }
        data = self.post("/v1/liquidity/add", params)
        transaction = data["tx"]
        # self.run_transaction(transaction)
        return data

    def remove_liquidity(self):
        pass

    def swap_tokens(self):
        pass