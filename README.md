cryptoCurrencyTrading
=====================

Some tools related to cryptocurrency trading

 

Tool1    exchange price monitoring 
-----------------------------------

This tool has two main functions

-   monitor the price between different exchanges and notify user if one
    exchange has big price drop or increase.

-   monitor the price history of specified coins, if the price at one exchange
    is increasing or decreasing rapidly, notify user.

-   currently supported exchanges: *bitfinex, bitflyer, bithumb, BTCCChina,
    coinone, gdax, huobi, kraken, OKcoin, OKcoinCN*

-   Current notification only supports email.

### How to use 

1.  change your email address at priceMonitoring/exchangeMonitoringRun.py

2.  change the coins you want to monitor at priceMonitoring/coinMain

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd priceMonitoring; python3 exchangeMonitoringRun.py; 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 
