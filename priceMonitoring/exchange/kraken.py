



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


class kraken: 
	supported_coin = {"BTC"}
	supported_trading_pairs = ['BCHEUR',  'BCHUSD',  'BCHXBT',  'DASHEUR',  'DASHUSD',  'DASHXBT',  'EOSETH',  'EOSXBT',  'GNOETH',  'GNOXBT',  'USDTZUSD',  'XETCXETH',  'XETCXXBT',  'XETCZEUR',  'XETCZUSD',  'XETHXXBT',  'XETHXXBT.d',  'XETHZCAD',  'XETHZCAD.d',  'XETHZEUR',  'XETHZEUR.d',  'XETHZGBP',  'XETHZGBP.d',  'XETHZJPY',  'XETHZJPY.d',  'XETHZUSD',  'XETHZUSD.d',  'XICNXETH',  'XICNXXBT',  'XLTCXXBT',  'XLTCZEUR',  'XLTCZUSD',  'XMLNXETH',  'XMLNXXBT',  'XREPXETH',  'XREPXXBT',  'XREPZEUR',  'XXBTZCAD',  'XXBTZCAD.d',  'XXBTZEUR',  'XXBTZEUR.d',  'XXBTZGBP',  'XXBTZGBP.d',  'XXBTZJPY',  'XXBTZJPY.d',  'XXBTZUSD',  'XXBTZUSD.d',  'XXDGXXBT',  'XXLMXXBT',  'XXMRXXBT',  'XXMRZEUR',  'XXMRZUSD',  'XXRPXXBT',  'XXRPZEUR',  'XXRPZUSD',  'XZECXXBT',  'XZECZEUR',  'XZECZUSD']
	
	@staticmethod
	def get_current_price(coin, currency_converter):
		price = -1 
		try: 
			if coin.lower() == "btc": 
				coin = "XBT"
			trading_pair = "{}EUR".format(coin.upper())
			for pair in kraken.supported_trading_pairs: 
				if "EUR" in pair and coin.upper() in pair: 
					trading_pair = pair 
					break 

			dat = json.loads(requests.get("https://api.kraken.com/0/public/Ticker", params={"pair": trading_pair} ).text)["result"][trading_pair]
			price = (float) (dat["c"][0]) / currency_converter.get_exchange_rate("EUR")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_buy_price(coin, currency_converter):
		price = -1 
		try: 
			if coin.lower() == "btc": 
				coin = "XBT"
			trading_pair = "{}EUR".format(coin.upper())
			for pair in kraken.supported_trading_pairs: 
				if "EUR" in pair and coin.upper() in pair: 
					trading_pair = pair 
					break 

			dat = json.loads(requests.get("https://api.kraken.com/0/public/Ticker", params={"pair": trading_pair} ).text)["result"][trading_pair]
			price = (float) (dat["b"][0]) / currency_converter.get_exchange_rate("EUR")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_sell_price(coin, currency_converter):
		price = -1 
		try: 
			if coin.lower() == "btc": 
				coin = "XBT"
			trading_pair = "{}EUR".format(coin.upper())
			for pair in kraken.supported_trading_pairs: 
				if "EUR" in pair and coin.upper() in pair: 
					trading_pair = pair 
					break 

			dat = json.loads(requests.get("https://api.kraken.com/0/public/Ticker", params={"pair": trading_pair} ).text)["result"][trading_pair]
			price = (float) (dat["a"][0]) / currency_converter.get_exchange_rate("EUR")
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return price 

	@staticmethod
	def get_one_day_volume(coin, currency_converter):
		vol = -1 
		try: 
			if coin.lower() == "btc": 
				coin = "XBT"
			trading_pair = "{}EUR".format(coin.upper())
			for pair in kraken.supported_trading_pairs: 
				if "EUR" in pair and coin.upper() in pair: 
					trading_pair = pair 
					break 

			dat = json.loads(requests.get("https://api.kraken.com/0/public/Ticker", params={"pair": trading_pair} ).text)["result"][trading_pair]
			vol = (float) (dat["v"][0]) 
		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return vol 

	@staticmethod 
	def get_trading_pair(): 
		market = []
		try: 
			dat = json.loads(requests.get("https://api.kraken.com/0/public/AssetPairs").text)["result"]
			market = list(dat.keys())

		except Exception as e:
			WARNING("{}: {}: {}".format(__name__, coin, e))
		return market 




	@staticmethod 
	def get_trading_pair_standard():
		pass 



	@staticmethod 
	def get_assests(): 
		pass 


if __name__ == "__main__": 
	cc = fiatCurrencyConverter()
	pprint(kraken.get_current_price("ETH", cc))
	pprint(kraken.get_current_price("BTC", cc))
	# pprint(kraken.get_trading_pair())
