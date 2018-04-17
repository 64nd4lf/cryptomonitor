import json
import urllib2

#loading currency data
curr_dat = json.load(open('curr_dat.json'))
mids = {}
markets = ["btc", "usdt", "ltc", "bch", "eth", "etc"]
mar_diff = {"Currency" : [], "Percentage difference" : []}
more_info = {"Currency" : '', "Buy" : [], "Sell" : [], "m_dat" : {}}

# Loading all the markets on coinexchange to find and build market IDs
hdr = {"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"}
url = 'https://www.coinexchange.io/api/v1/getmarkets'
req = urllib2.Request(url, headers = hdr)
resp = urllib2.urlopen(req)
content = json.load(resp)

#building market IDs for coinexchange
for x in curr_dat:
	for y in curr_dat[x]["exchanges"]:
		if(y == "cio"):
			for z in curr_dat[x]["exchanges"][y]:
				for k in range(len(content["result"])):
					if(content["result"][k]["MarketAssetCode"] == x and content["result"][k]["BaseCurrencyCode"] == z):
						mids["{}-{}".format(x, z)] = str(content["result"][k]["MarketID"])
#print(mids)

#Loading prices on cryptopia
url = 'https://www.cryptopia.co.nz/api/GetMarkets'
req = urllib2.Request(url)
resp = urllib2.urlopen(req)
content = resp.read()
with open('crpa-prices.json', 'w') as outfile:
	json.dump(content, outfile)

#Loading prices on tradesatoshi
url = "https://tradesatoshi.com/api/public/getmarketsummaries"
req = urllib2.Request(url, headers = hdr)
resp = urllib2.urlopen(req)
content = resp.read()
with open('tsat-prices.json', 'w') as outfile:
	json.dump(content, outfile)

#Loading prices on coinexchange
url = 'https://www.coinexchange.io/api/v1/getmarketsummaries'
req = urllib2.Request(url)
resp = urllib2.urlopen(req)
content = resp.read()
with open('cio-prices.json', 'w') as outfile:
	json.dump(content, outfile)

#Loading prices from hitBTC
url = 'https://api.hitbtc.com/api/2/public/ticker'
req = urllib2.Request(url)
resp = urllib2.urlopen(req)
content = resp.read()
with open('hbtc-prices.json', 'w') as outfile:
	json.dump(content, outfile)

# loading doge prices from coinmarketcap
for k in range(len(markets)):
	url = "https://api.coinmarketcap.com/v1/ticker/dogecoin/?convert={}".format(markets[k])
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req)
	content = json.load(resp)
	#print(float(content[0]["price_{}".format(markets[k])]))
	with open('ex-doge-{}.json'.format(markets[k]), 'w') as outfile:
		json.dump(content, outfile)

#coverting from all prices to doge
def btc(v):
	dat = json.load(open('ex-doge-btc.json'))
	value = float(dat[0]["price_btc"])
	#print(value)
	return v/value
def ltc(v):
	dat = json.load(open('ex-doge-ltc.json'))
	#udat = json.loads(dat)
	value = float(dat[0]["price_ltc"])
	#print(value)
	return v/value
def bch(v):
	dat = json.load(open('ex-doge-bch.json'))
	value = float(dat[0]["price_bch"])
	#print(value)
	return v/value
def etc(v):
	dat = json.load(open('ex-doge-etc.json'))
	value = float(dat[0]["price_etc"])
	#print(value)
	return v/value
def eth(v):
	dat = json.load(open('ex-doge-eth.json'))
	value = float(dat[0]["price_eth"])
	#print(value)
	return v/value
def usdt(v):
	dat = json.load(open('ex-doge-usdt.json'))
	value = float(dat[0]["price_usdt"])
	#print(value)
	return v/value
def nzdt(v):
	dat = json.load(open('crpa-prices.json'))
	udat = json.loads(dat)
	for k in range(len(udat["Data"])):
		if(udat["Data"][k]["Label"] == "DOGE/NZDT"):
			value = float(udat["Data"][k]["LastPrice"])
	#print(value)
	return v/value

#Comparing and building data to find profits
buy = []
sell = []
for x in curr_dat: #for each currency
	for y in curr_dat[x]["exchanges"]: #for each exchange a currency is available on
		if(y == "crpa"):
			dat = json.load(open('crpa-prices.json'))
			udat = json.loads(dat)
			for z in curr_dat[x]["exchanges"][y]: #for each base market a currency is tradable with, within an exchange
				for k in range(len(udat["Data"])): #traversing the json file which contains the prices
					if(udat["Data"][k]["Label"] == "{}/{}".format(x, z)): #finding and loading the price (buy and sell) of the current currency with current base market
						b_rate = float(udat["Data"][k]["BidPrice"]) 
						s_rate = float(udat["Data"][k]["AskPrice"])

				#converting prices to doge (to make comparison of prices easy)
				if(z == "BTC"):
					b_rate = btc(b_rate)
					s_rate = btc(s_rate)
				elif(z == "USDT"):
					b_rate = usdt(b_rate)
					s_rate = usdt(s_rate)
				elif(z == "LTC"):
					b_rate = ltc(b_rate)
					s_rate = ltc(s_rate)
				elif(z == "NZDT"):
					b_rate = nzdt(b_rate)
					s_rate = nzdt(s_rate)
				buy.append(b_rate)
				sell.append(s_rate)
		elif(y == "tsat"):
			dat = json.load(open('tsat-prices.json'))
			udat = json.loads(dat)
			for z in curr_dat[x]["exchanges"][y]: #for each base market a currency is tradable with, within an exchange
				for k in range(len(udat["result"])):
					if(udat["result"][k]["market"] == "{}_{}".format(x, z)):
						b_rate = float(udat["result"][k]["bid"])
						s_rate = float(udat["result"][k]["ask"])
				if(z == "BTC"):
					b_rate = btc(b_rate)
					s_rate = btc(s_rate)
				elif(z == "USDT"):
					b_rate = usdt(b_rate)
					s_rate = usdt(s_rate)
				elif(z == "LTC"):
					b_rate = ltc(b_rate)
					s_rate = ltc(s_rate)
				elif(z == "BCH"):
					b_rate = bch(b_rate)
					s_rate = bch(s_rate)
				buy.append(b_rate)
				sell.append(s_rate)
		elif(y == "cio"):
			dat = json.load(open('cio-prices.json'))
			udat = json.loads(dat)
			for z in curr_dat[x]["exchanges"][y]:
				for k in range(len(udat["result"])):
					if(udat["result"][k]["MarketID"] == mids["{}-{}".format(x, z)]):
						b_rate = float(udat["result"][k]["BidPrice"])
						s_rate = float(udat["result"][k]["AskPrice"])
				if(z == "BTC"):
					b_rate = btc(b_rate)
					s_rate = btc(s_rate)
				elif(z == "ETH"):
					b_rate = eth(b_rate)
					s_rate = eth(s_rate)
				elif(z == "LTC"):
					b_rate = ltc(b_rate)
					s_rate = ltc(s_rate)
				elif(z == "ETC"):
					b_rate = etc(b_rate)
					s_rate = etc(s_rate)
				buy.append(b_rate)
				sell.append(s_rate)
		elif(y == "hbtc"):
			dat = json.load(open('hbtc-prices.json'))
			udat = json.loads(dat)
			for z in curr_dat[x]["exchanges"][y]:
				for k in range(len(udat)):
					if(udat[k]["symbol"] == "{}{}".format(x, z)):
						if(udat[k]["bid"] == None):
							b_rate = 0.0
						else:
							b_rate = float(str(udat[k]["bid"]))
						if(udat[k]["ask"] == None):
							s_rate = 0.0
						else:
							s_rate = float(str(udat[k]["ask"]))
				if(z == "BTC"):
					b_rate = btc(b_rate)
					s_rate = btc(s_rate)
				elif(z == "ETH"):
					b_rate = eth(b_rate)
					s_rate = eth(s_rate)
				elif(z == "USDT"):
					b_rate = usdt(b_rate)
					s_rate = usdt(s_rate)

				#storing all the buy and sell prices
				buy.append(b_rate)
				sell.append(s_rate)
	#print(x)

	max_buy = max([w for w in buy if w != 0]) #finding the maximum price a currency can be sold
	min_sell = min([w for w in sell if w != 0]) #finding the minimum price a currency can be bought
	p_diff = ((max_buy - min_sell)/min_sell)*100 #percentage difference is the profit percentage of the transaction
	#storing the buy, sell and currency's avaliablity data onto a file
	mar_diff["Currency"].append(x)
	mar_diff["Percentage difference"].append(p_diff)
	more_info["Currency"] = x
	more_info["Buy"] = [str(l) for l in buy]
	more_info["Sell"] = [str(l) for l in sell] 
	more_info["m_dat"] = curr_dat[x]
	with open('mi-{}.txt'.format(x), 'w') as outfile:
		json.dump(more_info, outfile)

	#refreshing buy and sell arrays for next iteration
	del buy[:]
	del sell[:]

#generating html
keys = mar_diff.keys()
length = len(mar_diff[keys[0]])
items = ['<html><head><script src="sorttable.js"></script> <link rel="stylesheet" type="text/css" href="style.css"><title>CryptoMonitor</title></head><body>', '<table class="sortable">', '<tr>']
for k in keys:
	items.append('<td>%s</td>' % k)
items.append('</tr>')

for i in range(length):
	items.append('<tr>')
	for k in keys:
		items.append('<td><a target="_blank" style="text-decoration:none;" href="mi-{}.txt">{}</a></td>'.format(mar_diff['Currency'][i], mar_diff[k][i]))
	items.append('</tr>')

items.append('</table></body></html>')

items = '\n'.join(items)

f = open('index.html', 'w')
f.write(items)
f.close()
