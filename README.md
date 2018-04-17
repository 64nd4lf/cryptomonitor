# cryptomonitor
Cryptomonitor is a trade arbitrage finder between four difference trading paltforms, cryptopia, tradesatoshi, coinexchange and hitBTC. The common currencies between the four exchanges have been extracted and a json file, curr_dat, is built which stores the metadata about a currency - where it is available and with which base currencies in a website it is tradeable. 

The program first loads the buy sell data of every currency on each website to four files, each representing prices on one of the four websites. Later curr_dat is traversed to load the best buy and sell prices of each currency onto two different lists, buy[] and sell[]. The highest buy rate(the maximum price a currency can be sold for) and the least sell rate (the minimum price a currency can be bought for) is calculated from the buy[] and sell[] lists. And then the % profit is determined. 

The best buy and sell rates are calculated for every currency listed on curr_data is computed and then stored onto a file. A html file is built which displays each currency and the %profit that we can gain by buy and sell that currency. We can sort this table based on the %profits. Each item on the table is a hyperlink which takes us to another page in a new tab that displays detailed info and from which we can know from where to buy for cheapest and sell for highest price. 

The latest code is 8 times faster and computes 4 times as many currencies as the previous one. I have reduced the HTTP requests in the code which slowed down the execution time in the first place.

I have created an EC2 micro instance on AWS and uploaded this code to the instance. I have scheduled a cronjob using crontab to run this build.py code every two minutes. So every two minutes the prices will be updated. I turn on the instance when I have time and look for any profitable trades and then turn the instance off when I don't want to monitor.

Warning: Sometimes currencies will be in maintenance during which period you can't deposit or withdraw money. So before making a transaction, make sure the currency's wallet is up and active on both the websites.
