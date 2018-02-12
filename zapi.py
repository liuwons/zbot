import requests


suc_codes = ["1000"]

errcode = {
    "1000": "success",
    "1001": "normal error",
    "1002": "internal error",
    "1003": "verify not passed",
    "1004": "fund security password locked",
    "1005": "fund security password not right",
    "1006": "real-name authentication verifying or not passed",
    "1009": "current api not in service",
    "2001": "RMB not sufficient",
    "2002": "BTC not sufficient",
    "2003": "LTC not sufficient",
    "2005": "ETH not sufficient",
    "2006": "ETC not sufficient",
    "2007": "BTS not sufficient",
    "2009": "balance not sufficient",
    "3001": "order not found",
    "3002": "invalid amount of money",
    "3003": "invalid count",
    "3004": "user not exists",
    "3005": "illegal argument",
    "3006": "IP error",
    "3007": "time expired",
    "3008": "trade history not found",
    "4001": "API locked or not opened",
    "4002": "requests too frequently"
}


class ZApi:
    def __init__(self):
        pass

    def ticker(self):
        pass

    def depth(self):
        pass

    def trades(self):
        pass

    def kline(self):
        pass

    def order(self):
        pass

    def cancel_order(self):
        pass

    def get_order(self):
        pass

    def get_orders(self):
        pass

    def get_orders_new(self):
        pass

    def get_orders_ignore_tader_type(self):
        pass

    def get_unfinished_orders_ignore_trade_type(self):
        pass

    def get_account_info(self):
        pass

    def get_user_address(self):
        pass

    def get_withdraw_address(self):
        pass

    def get_withdraw_record(self):
        pass

    def get_charge_record(self):
        pass

    def withdraw(self):
        pass

