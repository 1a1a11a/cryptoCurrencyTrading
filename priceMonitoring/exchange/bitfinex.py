

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



# [
#   BID, 
#   BID_SIZE, 
#   ASK, 
#   ASK_SIZE, 
#   DAILY_CHANGE, 
#   DAILY_CHANGE_PERC, 
#   LAST_PRICE, 
#   VOLUME, 
#   HIGH, 
#   LOW
# ]


class bitfinex: 
	supported_coin = {"ETH", "BTC", "LTC", "ETC"}
	@staticmethod
	def get_current_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.bitfinex.com/v2/ticker/t{}USD".format(coin.upper())).text)
			price = (float) (dat[6]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_buy_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.bitfinex.com/v2/ticker/t{}USD".format(coin.upper())).text)
			price = (float) (dat[2]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_sell_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://api.bitfinex.com/v2/ticker/t{}USD".format(coin.upper())).text)
			price = (float) (dat[0]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 


	@staticmethod
	def get_one_day_volume(coin, currency_converter):
		vol = -1 
		try: 
			dat = json.loads(requests.get("https://api.bitfinex.com/v2/ticker/t{}USD".format(coin.upper())).text)
			vol = (float) (dat[7]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return vol 




if __name__ == "__main__": 
	cc = fiatCurrencyConverter()
	pprint(bitfinex.get_current_price("ETH", cc))
