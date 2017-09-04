import requests 
import os, sys, time 
from collections import defaultdict, deque


sys.path.append("../lib")
sys.path.append("./")
sys.path.append("exchange")
from utilEmail import * 
from utilPrinting import * 
from coinbin import * 

from fiat import fiatCurrencyConverter 

from bitfinex import bitfinex 
from bitflyer import bitflyer 
from bithumb import bithumb 
from BTCCChina import BTCCChina 
from coinone import coinone 
from gdax import GDAX 
from huobi import huobi 
from kraken import kraken 
from OKcoin import OKcoin 
from OKcoinCN import OKcoinCN 


RECEIVER = "peter.waynechina@gmail.com"
EXCHANGE_LIST = [bitfinex, bitflyer, bithumb, BTCCChina, coinone, GDAX, huobi, kraken, OKcoin, OKcoinCN] 
OUTPUT_FOLDER = "priceLog/"

def alert(msg, topic="coin price alert"):
	""" send an email alerting user about price change 
		
	Arguments:
		msg {str} -- Email content
	
	Keyword Arguments:
		topic {str} -- Email Title (default: {"coin price alert"})
	"""
	defaultEmailClient().send_email(message=msg, topic=topic, receiver=RECEIVER) 


def get_coin_price_from_all_exchange(exchange_list, coins, fcc): 
	"""get coin prices from all the exchanges 
	
	Arguments:
		exchange_list {list} -- a list of exchanges 
		coins {list} -- a list of coins 
		fcc {[fiatCurrencyConverter]} -- an instance of fiatCurrencyConverter
	
	Returns:
		dict -- a dict in the form: coin -> {exchange -> price} 
	"""
	coin_price_dict = defaultdict(dict) 		# coin -> {exchange -> price} 
	for coin in coins: 
		for exchange in exchange_list: 
			coin_price_dict[coin][exchange] = round(exchange.get_current_price(coin, fcc), 2)

	return coin_price_dict 


def write_coin_price(output_file_dict, exchange_list, coin_price_dict): 
	""" output coin price to files, each coin corresponds to a file, 
		each line in the file corresponding to the price of the same coin from different exchanges 

	Arguments:
		output_file_dict {dict} -- a dict in the form: coin -> file pointer   
		exchange_list {list} -- a list of exchanges 
		coin_price_dict {dict} -- a dict in the form: coin -> {exchange -> price} 
	
	Returns:
		None 
	""" 

	for coin, exchange_price in coin_price_dict.items(): 
		line = "\t".join([str(exchange_price[exchange]) for exchange in exchange_list])
		output_file_dict[coin].write("{}\t{}\n".format(time.strftime("%Y-%m-%d#%H:%M:%S", 
																		time.localtime(time.time())), line))
		output_file_dict[coin].flush()


def analyze_coin_price_between_exchanges(coin, coin_prices_deque, exchange_list, 
											coin_last_ratio_dict, alert_threshold=0.03): 
	""" analyze the coin price difference between exchanges 
	
	[description]
	
	Arguments:
		coin {str} -- the coin to analyze, should be one from the coin_list
		coin_prices_deque {dict} -- a dict of form coin -> {exchange -> price_deque}
		exchange_list {list} -- a list of exchanges 
		coin_last_ratio_dict {dict} -- a dict of form coin -> {exchange1-exchange2 -> last_price_ratio}
	
	Keyword Arguments:
		alert_threshold {number} -- how much change between exchange price is allowed before alert (default: {0.03})
	
	Returns:
		str -- the alert message, if no alert, then empty string 
	"""
	exchange_prices = coin_prices_deque[coin]		# exchange -> price 
	last_ratio_dict = coin_last_ratio_dict[coin]
	topic = "{} exchnage price alert".format(coin)
	msg = ""

	for i in range(len(exchange_list)): 
		for j in range(i+1, len(exchange_list)): 
			exchange1 = exchange_list[i]
			exchange2 = exchange_list[j]
			if exchange_prices[exchange1][-1] == -1 or exchange_prices[exchange2][-1] == -1: 
				continue 

			new_ratio = exchange_prices[exchange1][-1] / exchange_prices[exchange2][-1]
			old_ratio = last_ratio_dict["{}-{}".format(exchange1.__name__, exchange2.__name__)]
			last_ratio_dict["{}-{}".format(exchange1.__name__, exchange2.__name__)] = new_ratio
			if old_ratio == 0 or abs(new_ratio - old_ratio) / old_ratio > alert_threshold: 
				msg += "<br><br>\r\n\r\n{} exchange: {}, old ratio: {}, new ratio: {}\r\n\r\n<br><br>prices: {}".format(coin, 
					"{}-{}".format(exchange1.__name__, exchange2.__name__), 
					old_ratio, new_ratio, 
					", ".join(["{}: {}".format(exchange.__name__, list(exchange_prices[exchange])) for exchange in list(exchange_prices.keys())]))
				break 
	return msg 



def analyze_coin_price_history(coin, exchange, coin_prices_deque, alert_threshold=0.05): 
	""" analyze coin history and alert user when the new price has exceeded thresh
		
	Arguments:
		coin {str} -- the coin to analyze, should be one from the coin_list
		exchange {str} -- the exchange which the price comes from 
		coin_prices_deque {dict} -- a dict of form coin -> {exchange -> price_deque}
	
	Keyword Arguments:
		alert_threshold {number} -- how much change between exchange price is allowed before alert (default: {0.05})
	
	Returns:
		str -- the alert message, if no alert, then empty string 
	"""
	price_history = coin_prices_deque[coin][exchange]
	msg = "" 
	if len(price_history) < 5: 
		return msg 

	try: 
		if abs(price_history[-1] - price_history[0]) / price_history[0] > alert_threshold: 
			msg += "\r\n\r\n{} price alert at exchange {}\r\n\r\n".format(coin, exchange.__name__, price_history)
	except Exception as e: 
		WARNING(e)

	return msg 


def run(coin_file="coin", price_compare_interval=3600, sleep_time=10, min_alert_interval=1200): 
	""" runnable function 
		
	Keyword Arguments:
		coin_file {str} -- the loc of file containing all coins (default: {"coin"})
		price_compare_interval {number} -- current price compared to price_compare_interval seconds ago (default: {3600})
		sleep_time {number} -- the time to sleep between each check (default: {10})
		min_alert_interval {number} -- ask the system to send out less alert, after the previous alert, it will wait for 
			min_alert_interval seconds before sending next alert (default: {1200})
	"""

	if not os.path.exists(OUTPUT_FOLDER): 
		os.makedirs(OUTPUT_FOLDER)


	coin_list = load_coin(coin_file)							# the list of coins to monitor 
	coin_prices_deque = defaultdict(dict) 						# coin -> deque(price_list of fixed size)
	# coin -> {exhange-exchange -> its price ratio} 
	coin_last_ratio_dict = {coin: defaultdict(float) for coin in coin_list}		

	fcc = fiatCurrencyConverter()								# for converting currency 
	exchange_list = EXCHANGE_LIST 								# a list of exchanges 

	# a dict coin -> coin_price_file_pointer 
	output_file_dict = {coin: open("{}/{}.price.exchange".format(OUTPUT_FOLDER, coin), "a") for coin in coin_list} 
	
	# time of last alert 
	last_alert_time = 0 

	# initialize file header 
	for coin, file in output_file_dict.items(): 
		if file.tell() == 0: 
			file.write("time          \t{}\n".format( "\t".join( [exchange.__name__ for exchange in  exchange_list] ) ))

	while 1:
		topic = ""
		all_msg = ""
		have_exchange_alert = False 
		have_price_history_alert = False 

		coin_price_dict = get_coin_price_from_all_exchange(exchange_list, coin_list, fcc)
		write_coin_price(output_file_dict, exchange_list, coin_price_dict)
		for coin in coin_list:
			for exchange in exchange_list: 
				if exchange in coin_prices_deque[coin]: 
					coin_prices_deque[coin][exchange].append(coin_price_dict[coin][exchange])
					coin_prices_deque[coin][exchange].popleft() 
				else: 
					coin_prices_deque[coin][exchange] = deque([coin_price_dict[coin][exchange]])

				msg = analyze_coin_price_history(coin, exchange, coin_prices_deque)
				if msg: 
					have_price_history_alert = True 
					all_msg += "<br><br><br><br><br><br><br>" + msg 

			msg = analyze_coin_price_between_exchanges(coin, coin_prices_deque, exchange_list, coin_last_ratio_dict)
			# pprint("{} {}".format(coin, msg))
			if msg: 
				have_exchange_alert = True 
				all_msg += "<br><br><br><br><br><br><br>" + msg 
		# print("{}\n{}".format(time.strftime("%H:%M:%S", time.localtime(time.time())), msg))


		if len(msg) and time.time() - last_alert_time >= min_alert_interval: 
			topic = "alert "
			if have_exchange_alert: 
				topic += "exchange, "
			if have_price_history_alert: 
				topic += "history"
			alert(msg=all_msg, topic=topic)
			last_alert_time = time.time() 

		time.sleep(sleep_time) 

	for file in output_file_dict.values(): 
		file.close() 


def load_coin(coin_file):
	""" load monitoring coin symbols from file 
	
	
	Arguments:
		coin_file {str} -- the loc of file 
	
	Returns:
		list -- a list of coins 
	"""
	coin_list = []
	with open(coin_file) as ifile: 
		for line in ifile: 
			coin_list.append(line.strip("\n"))

	return coin_list 




if __name__ == "__main__": 
	# alert("test msg")
	run(coin_file="coinMain", price_compare_interval=300, sleep_time=5, min_alert_interval=1200)

