

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


class bitflyer: 
	supported_coin = {"BTC"}
	notsupported_coinss = {"ETH", "LTC"}

	@staticmethod
	def get_current_price(coin, currency_converter):
		if coin.upper() in bitflyer.notsupported_coinss: 
			return -1
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.bitflyer.jp/v1/getticker", params={"product_code": "{}_JPY".format(coin.upper())} ).text)
			price = ((float) (dat["best_bid"]) + (float) (dat["best_ask"])) / 2 / currency_converter.get_exchange_rate("JPY")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_buy_price(coin, currency_converter):
		if coin.upper() in bitflyer.notsupported_coins: 
			return -1
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.bitflyer.jp/v1/getticker", params={"product_code": "{}_JPY".format(coin.upper())} ).text)
			price = (float) (dat["best_bid"]) /currency_converter.get_exchange_rate("JPY")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_sell_price(coin, currency_converter):
		if coin.upper() in bitflyer.notsupported_coins: 
			return -1
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.bitflyer.jp/v1/getticker", params={"product_code": "{}_JPY".format(coin.upper())} ).text)
			price = (float) (dat["best_ask"]) /currency_converter.get_exchange_rate("KRW")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_one_day_volume(coin, currency_converter):
		if coin.upper() in bitflyer.notsupported_coins: 
			return -1
		vol = -1 
		try: 
			dat = json.loads(requests.get("https://api.bitflyer.jp/v1/getticker", params={"product_code": "{}_JPY".format(coin.upper())} ).text)
			vol = (float) (dat["volume"]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return vol 

	@staticmethod 
	def get_market(): 
		market = []
		try: 
			dat = json.loads(requests.get("https://api.bitflyer.jp/v1/markets").text)[0]
			for k, v in dat.items(): 
				market.append(dat["product_code"])

		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return market 




	@staticmethod 
	def get_market_standard():
		pass 




if __name__ == "__main__": 
	cc = fiatCurrencyConverter()
	# pprint(bitflyer.get_current_price("ETH", cc))
	pprint(bitflyer.get_current_price("BTC", cc))
	bitflyer.get_market()
