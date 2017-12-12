import json
import urllib2

curr_dat = {"trc":{"exchanges":{"crpa":3, "tsat":4, "cio":['btc']}}, "bun":{"exchanges":{"crpa":2, "tsat":4}}, "pura":{"exchanges":{"crpa":3, "cio":['btc', 'eth']}}, "piggy":{"exchanges":{"crpa":3, "tsat":4, "cio":['btc']}}, "rbbt":{"exchanges":{"crpa":2}}, "nka":{"exchanges":{"crpa":3, "tsat":4}}, "sha":{"exchanges":{"crpa":3, "tsat":4}}, "dcn":{"exchanges":{"crpa":3, "cio":['btc', 'eth']}}, "nyan":{"exchanges":{"crpa":3, "tsat":4}}, "riya":{"exchanges":{"crpa":3, "cio":['btc']}}, "emc2":{"exchanges":{"crpa":3, "tsat":4}}, "808":{"exchanges":{"crpa":3, "tsat":4}}, "kayi":{"exchanges":{"crpa":3, "cio":['btc', 'eth', 'doge']}}, "611":{"exchanges":{"crpa":3, "tsat":4, "cio":['btc']}}, "comp":{"exchanges":{"crpa":3, "tsat":4}}, "net":{"exchanges":{"crpa":3, "tsat":4}}, "rdd":{"exchanges":{"crpa":3, "tsat":4}}, "kmd":{"exchanges":{"crpa":3, "tsat":4, "cio":['btc', 'eth']}}}
tsat_mar = ['btc', 'bch', 'ltc', 'doge']
markets = ['btc', 'ltc', 'bch', 'eth', 'etc']
mar_diff = {"Currency" : [], "Percentage difference" : []}
more_info = {"Currency" : '', "Buy" : [], "Sell" : [], "m_dat" : {}}

#cryptopia price load
crpa_curr = ['trc', 'pura', 'piggy', 'nka', 'sha', 'dcn', 'nyan', 'riya', 'emc2', '808', 'kayi', '611', 'comp', 'net', 'rdd', 'kmd']
for base_curr in range(len(crpa_curr)):
	url = 'https://www.cryptopia.co.nz/api/GetMarketOrderGroups/{}_btc-{}_ltc-{}_doge/1'.format(crpa_curr[base_curr], crpa_curr[base_curr], crpa_curr[base_curr])
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req)
	content = resp.read()
	with open('crpa-{}.json'.format(crpa_curr[base_curr]), 'w') as outfile:
		json.dump(content, outfile)

#cryptopia ltc-and-doge-markets only currencies price load
crpa_ld_curr = ['bun', 'rbbt']
for base_curr in range(len(crpa_ld_curr)):
	url = 'https://www.cryptopia.co.nz/api/GetMarketOrderGroups/{}_ltc-{}_doge/1'.format(crpa_ld_curr[base_curr], crpa_ld_curr[base_curr])
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req)
	content = resp.read()
	with open('crpa-{}.json'.format(crpa_ld_curr[base_curr]), 'w') as outfile:
		json.dump(content, outfile)

#tradesatoshi price load
tsat_curr = ['trc', 'bun', 'piggy', 'nka', 'sha', 'nyan', 'emc2', '808', '611', 'comp', 'net', 'rdd', 'kmd']
for curr_curr in range(len(tsat_curr)):
	b_currs = ['btc', 'ltc', 'doge', 'bch']
	hdr = {"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"}
	for base_curr in range(len(b_currs)):
		url = "https://tradesatoshi.com/api/public/getticker?market={}_{}".format(tsat_curr[curr_curr], b_currs[base_curr])
		req = urllib2.Request(url, headers = hdr)
		resp = urllib2.urlopen(req)
		content = resp.read()
		with open('tsat-{}-{}.json'.format(tsat_curr[curr_curr], b_currs[base_curr]), 'w') as outfile:
			json.dump(content, outfile)

#coinexchange price load
mids = {"trc-btc":474, "pura-btc":57, "pura-eth":434, "piggy-btc":63, "qtum-btc":574, "qtum-eth":575, "dcn-btc":480, "dcn-eth":481, "riya-btc":431, "kayi-btc":505, "kayi-eth":506, "kayi-doge":507, "611-btc":351, "acc-btc":498, "kmd-btc":231, "kmd-eth":317}
for mid in mids:
	url = 'https://www.coinexchange.io/api/v1/getmarketsummary?market_id={}'.format(mids[mid])
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req)
	content = resp.read()
	with open('cio-{}.json'.format(mid), 'w') as outfile:
		json.dump(content, outfile)

#getting exchange rates
for k in range(len(markets)):
	url = "https://api.cryptonator.com/api/ticker/doge-{}".format(markets[k])
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req)
	content = resp.read()
	with open('ex-doge-{}.json'.format(markets[k]), 'w') as outfile:
		json.dump(content, outfile)

#covert to doge
def btc(v):
	dat = json.load(open('ex-doge-btc.json'))
	udat = json.loads(dat)
	value = float(udat["ticker"]["price"])
	return v/value
def ltc(v):
	dat = json.load(open('ex-doge-ltc.json'))
	udat = json.loads(dat)
	value = float(udat["ticker"]["price"])
	return v/value
def bch(v):
	dat = json.load(open('ex-doge-bch.json'))
	udat = json.loads(dat)
	value = float(udat["ticker"]["price"])
	return v/value
def etc(v):
	dat = json.load(open('ex-doge-etc.json'))
	udat = json.loads(dat)
	value = float(udat["ticker"]["price"])
	return v/value
def eth(v):
	dat = json.load(open('ex-doge-eth.json'))
	udat = json.loads(dat)
	value = float(udat["ticker"]["price"])
	return v/value

#comparing markets
buy = []
sell = []
for x in curr_dat:
	#print "{}: ".format(x)
	for y in curr_dat[x]:
		for z in curr_dat[x][y]:
			if z == 'cio':
				for k in curr_dat[x][y][z]:
					#print "{}-{}-{}".format(z, x, k)
					dat = json.load(open('{}-{}-{}.json'.format(z, x, k)))
					udat = json.loads(dat)
					b_rate = float(udat["result"]["BidPrice"])
					s_rate = float(udat["result"]["AskPrice"])
					if k != 'doge':
						b_rate = eval(k)(b_rate)
						s_rate = eval(k)(s_rate)
					buy.append(b_rate)
					sell.append(s_rate)
			elif z == 'tsat':
				#print "All four"
				for k in range(0, 4):
					dat = json.load(open('{}-{}-{}.json'.format(z, x, tsat_mar[k])))
					udat = json.loads(dat)
					b_rate = float(udat["result"]["bid"])
					s_rate = float(udat["result"]["ask"])
					if tsat_mar[k] != 'doge':
						b_rate = eval(tsat_mar[k])(b_rate)
						s_rate = eval(tsat_mar[k])(s_rate)
					buy.append(b_rate)
					sell.append(s_rate)
			else:
				if curr_dat[x][y][z] == 3:
					#print "All three"
					dat = json.load(open('{}-{}.json'.format(z, x)))
					udat = json.loads(dat)
					for k in range(0, 3):
						if len(udat["Data"][k]["Buy"]) != 0:
							b_rate = float(udat["Data"][k]["Buy"][0]["Price"])
						else:
							b_rate = 0.0
						if len(udat["Data"][k]["Sell"]) != 0:
							s_rate = float(udat["Data"][k]["Sell"][0]["Price"])
						else:
							s_rate = 0.0
						if k == 0:
							b_rate = btc(b_rate)
							s_rate = btc(s_rate)
						elif k == 2:
							b_rate = ltc(b_rate)
							s_rate = ltc(s_rate)
						buy.append(b_rate)
						sell.append(s_rate)
				else:
					#print "Only two"
					dat = json.load(open('{}-{}.json'.format(z, x)))
					udat = json.loads(dat)
					for k in range(0, 2):
						if len(udat["Data"][k]["Buy"]) != 0:
							b_rate = float(udat["Data"][k]["Buy"][0]["Price"])
						else:
							b_rate = 0.0
						if len(udat["Data"][k]["Sell"]) != 0:
							s_rate = float(udat["Data"][k]["Sell"][0]["Price"])
						else:
							s_rate = 0.0
						if k == 1:
							b_rate = ltc(b_rate)
							s_rate = ltc(s_rate)
						buy.append(b_rate)
						sell.append(s_rate)
	#print buy
	#print sell
	max_buy = max([w for w in buy if w != 0])
	min_sell = min([w for w in sell if w != 0])
	p_diff = ((max_buy - min_sell)/min_sell)*100
	mar_diff["Currency"].append(x)
	mar_diff["Percentage difference"].append(p_diff)
	more_info["Currency"] = x
	more_info["Buy"] = buy
	more_info["Sell"] = sell
	more_info["m_dat"] = curr_dat[x]
	#print "B - {}, S-{}".format(min_sell, max_buy)
	with open('mi-{}.txt'.format(x), 'w') as outfile:
		json.dump(more_info, outfile)
	del buy[:]
	del sell[:]
	#print "----------------------"
print mar_diff

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

items.append('</table></body>')

items = '\n'.join(items)

f = open('index.html', 'w')
f.write(items)
f.close()