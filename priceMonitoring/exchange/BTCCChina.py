
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


class BTCCChina: 
	supported_coin = {"ltccny", "btccny"}
	notsupported_coins = {"ETH"}
	# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}

	@staticmethod
	def get_current_price(coin, currency_converter):
		if coin.upper() in BTCCChina.notsupported_coins:
			return -1 

		price = -1 
		try: 
			dat = json.loads(requests.get("https://data.btcchina.com/data/ticker", 
											params={"market": "{}cny".format(coin.lower())}).text)["ticker"]
			price = (float) (dat["last"]) / currency_converter.get_exchange_rate("CNY")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_buy_price(coin, currency_converter):
		if coin.upper() in BTCCChina.notsupported_coins: 
			return -1 

		price = -1 
		try: 
			dat = json.loads(requests.get("https://data.btcchina.com/data/ticker", 
											params={"market": "{}cny".format(coin.lower())}).text)["ticker"]
			price = (float) (dat["buy"]) / currency_converter.get_exchange_rate("CNY")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_sell_price(coin, currency_converter):
		if coin.upper() in BTCCChina.notsupported_coins: 
			return -1 

		price = -1 
		try: 
			dat = json.loads(requests.get("https://data.btcchina.com/data/ticker", 
											params={"market": "{}cny".format(coin.lower())}).text)["ticker"]
			price = (float) (dat["sell"]) / currency_converter.get_exchange_rate("CNY")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 


	@staticmethod
	def get_one_day_volume(coin, currency_converter):
		if coin.upper() in BTCCChina.notsupported_coins: 
			return -1 

		vol = -1 
		try: 
			dat = json.loads(requests.get("https://data.btcchina.com/data/ticker", 
											params={"market": "{}cny".format(coin.lower())}).text)["ticker"]
			vol = (float) (dat["vol"]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return vol 





if __name__ == "__main__": 
	cc = fiatCurrencyConverter()
	pprint(BTCCChina.get_current_price("LTC", cc))
	pprint(BTCCChina.get_current_price("BTC", cc))

