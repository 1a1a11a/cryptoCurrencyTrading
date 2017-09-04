

import os 
import sys 
import time 
import json 
import requests 
from pprint import pprint, pformat 


sys.path.append("../../lib")
sys.path.append("./")
from utilEmail import * 
from utilPrinting import * 
from fiat import fiatCurrencyConverter 


class coinone: 
	supported_coin = {"btc", "bch", "eth", "etc", "xrp", "qtum", "all"}
	notsupported_coins = {"LTC"}

	@staticmethod
	def get_current_price(coin, currency_converter):
		if coin.upper() in coinone.notsupported_coins: 
			return -1 

		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.coinone.co.kr/ticker/", params={"currency":coin.lower(), "format": "json"}).text)
			price = (float) (dat["last"]) /currency_converter.get_exchange_rate("KRW")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_buy_price(coin, currency_converter):
		if coin.upper() in coinone.notsupported_coins: 
			return -1 

		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.coinone.co.kr/ticker/", params={"currency":coin.lower(), "format": "json"}).text)
			price = (float) (dat["last"]) /currency_converter.get_exchange_rate("KRW")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_sell_price(coin, currency_converter):
		if coin.upper() in coinone.notsupported_coins: 
			return -1 

		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.coinone.co.kr/ticker/", params={"currency":coin.lower(), "format": "json"}).text)
			price = (float) (dat["last"]) /currency_converter.get_exchange_rate("KRW")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_one_day_volume(coin, currency_converter):
		if coin.upper() in coinone.notsupported_coins: 
			return -1 

		vol = -1 
		try: 
			dat = json.loads(requests.get("https://api.coinone.co.kr/ticker/", params={"currency":coin.lower(), "format": "json"}).text)
			vol = (float) (dat["volume"]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return vol 





if __name__ == "__main__": 
	cc = fiatCurrencyConverter()
	pprint(coinone.get_current_price("ETH", cc))
