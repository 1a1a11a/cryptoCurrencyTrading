

import os 
import sys 
import time 
import json 
import requests 
from pprint import pprint, pformat 


sys.path.append("../../lib")
sys.path.append("./")
from utilPrinting import * 




class fiatCurrencyConverter: 
	def __init__(self):
		self.rates = {"KRW": 1130, "CNY": 6.53, "JPY": 109.65}
		self.last_check_time = 0 


	def update(self):
		self.last_check_time = time.time() 
		try: 
			dat = json.loads(requests.get("http://api.fixer.io/latest", params={"base":"USD"}).text)["rates"]
			if len(dat) > 0: 
				self.rates = dat
		except Exception as e: 
			WARNING(e) 


	def get_exchange_rate(self, currency): 
		if time.time() - self.last_check_time > 3600: 
			self.update() 
		return self.rates.get(currency, -1)
		# return getattr(self.rates, currency, -1)




if __name__ == "__main__": 
	fcc = fiatCurrencyConverter()
	fcc.update()
	print(fcc.get_exchange_rate("CNY"))
