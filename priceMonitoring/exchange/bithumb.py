
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


class bithumb: 
	supported_coin = {"ETH", "BTC", "LTC", "DASH", "ETC", "XRP", "BCH", "XMR"}
	notsupported_coin = {}
	
	@staticmethod
	def get_current_price(coin, currency_converter):
		if coin.upper() in bithumb.notsupported_coin: 
			return -1
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.bithumb.com/public/ticker/{}".format(coin)).text)["data"]
			price = ((float) (dat["buy_price"]) + (float) (dat["sell_price"]))/2/currency_converter.get_exchange_rate("KRW")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_buy_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.bithumb.com/public/ticker/{}".format(coin)).text)["data"]
			price = (float) (dat["buy_price"]) / currency_converter.get_exchange_rate("KRW")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_sell_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.bithumb.com/public/ticker/{}".format(coin)).text)["data"]
			price = (float) (dat["sell_price"]) / currency_converter.get_exchange_rate("KRW")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 






if __name__ == "__main__": 
	cc = fiatCurrencyConverter()
	pprint(bithumb.get_current_price("ETH", cc))
