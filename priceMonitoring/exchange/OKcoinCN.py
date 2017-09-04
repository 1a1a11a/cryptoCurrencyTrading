

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


class OKcoinCN: 
	supported_coin = {"ETH", "BTC", "LTC", "ETC", "BCC"}
	@staticmethod
	def get_current_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://www.okcoin.cn/api/v1/ticker.do?symbol={}_cny".format(coin.lower())).text)["ticker"]
			# pprint(dat)
			price = ((float) (dat["buy"]) + (float) (dat["sell"])) / 2 / currency_converter.get_exchange_rate("CNY")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_buy_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://www.okcoin.cn/api/v1/ticker.do?symbol={}_cny".format(coin.lower())).text)["ticker"]
			price = (float) (dat["buy"]) / currency_converter.get_exchange_rate("CNY")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_sell_price(coin, currency_converter):
		price = -1 
		try: 
			dat = json.loads(requests.get("https://www.okcoin.cn/api/v1/ticker.do?symbol={}_cny".format(coin.lower())).text)["ticker"]
			price = (float) (dat["sell"]) / currency_converter.get_exchange_rate("CNY")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 


	@staticmethod
	def get_one_day_volume(coin, currency_converter):
		vol = -1 
		try: 
			dat = json.loads(requests.get("https://www.okcoin.cn/api/v1/ticker.do?symbol={}_cny".format(coin.lower())).text)["ticker"]
			vol = (float) (dat["vol"]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return vol 





if __name__ == "__main__": 
	cc = fiatCurrencyConverter()
	pprint(OKcoinCN.get_current_price("ETH", cc))
