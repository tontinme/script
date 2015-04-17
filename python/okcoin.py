#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import urllib
import random
from subprocess import *

minPrice = float("25.00")
maxPrice = float("240.00")
ratePrice = float("0.100")
curTime=time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))

#last_price
if not ( os.path.isfile("./lastPrice.tmp")) or (os.stat("./lastPrice.tmp").st_size == 0):
  last_price = float("1.00")
else:
  tmp_file = open("./lastPrice.tmp", 'r')
  last_priceList = tmp_file.readlines()
  last_price_tmp = last_priceList[0]
  last_price = float(last_price_tmp)
  tmp_file.close()

#ltc_price
rand = random.randint(10,99)
url_dest = "https://www.okcoin.com/real/ticker.do?random=%d" %(rand)
context = urllib.urlopen(url_dest)
content_Dict = eval(context.read())
btc_price_tmp = content_Dict['btcLast']
btc_price = float(btc_price_tmp)
ltc_price_tmp = content_Dict['ltcLast']
ltc_price = float(ltc_price_tmp)

tmp_file = open("./lastPrice.tmp", 'w')
tmp_file.write(ltc_price_tmp)
tmp_file.close()

rate_price_tmp = "%.3f" % (abs(ltc_price - last_price) / last_price)
rate_price = float(rate_price_tmp)
sms_msg = "[OKCoin] Now price: %s, last price: %s, Change rate: %s" %(ltc_price, last_price, rate_price)
#url = "http://sms.freesms.xxx/send.php?appid=default&%s" % urllib.urlencode(sms_msg)
url = "http://freesmsORemail/service/?c=sms+Your_Address+'%s'" % sms_msg

if ( ltc_price <= minPrice ) or ( ltc_price >= maxPrice ) or ( rate_price >= ratePrice ):
  send_msg = "wget -O /dev/null --timeout=10 --tries=3 %s >/dev/null 2>&1" % url
  output = Popen(send_msg, shell=True).communicate()[0]
print_msg = "[%s] [OKCoin] Now ltcPrice: %s, Last ltcPrice: %s, Change Rate: %s..---.. Now btcPrice: %s" %(curTime,ltc_price,last_price,rate_price,btc_price)
print "%s" % print_msg

context.close()
