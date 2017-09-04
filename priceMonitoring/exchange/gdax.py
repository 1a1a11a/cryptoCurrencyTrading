

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




class GDAX: 
	supported_coin = {"ETH", "BTC", "LTC"}

	@staticmethod
	def get_current_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.gdax.com/products/{}-USD/ticker".format(coin.upper())).text)
			price = ( (float) (dat["bid"]) + (float) (dat["ask"]) ) / 2 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_buy_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.gdax.com/products/{}-USD/ticker".format(coin.upper())).text)
			price =  (float) (dat["bid"]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_sell_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.gdax.com/products/{}-USD/ticker".format(coin.upper())).text)
			price = (float) (dat["ask"]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 


	@staticmethod
	def get_one_day_volume(coin, currency_converter):
		vol = -1 
		try: 
			dat = json.loads(requests.get("https://api.gdax.com/products/{}-USD/ticker".format(coin.upper())).text)
			vol = (float) (dat["volume"]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return vol 





if __name__ == "__main__": 
	cc = fiatCurrencyConverter()
	pprint(GDAX.get_current_price("ETH", cc))
