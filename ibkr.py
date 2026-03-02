import threading
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

preturn = 0

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
	def tickPrice(self, reqId, tickType, price, attrib):
		global preturn

		if tickType == 2 and reqId == 1:
			preturn = price
	
def run_loop():
	app.run()

app = IBapi()
app.connect('N/A', 4002, 887888)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = 'USD'
eurusd_contract.secType = 'CASH'
eurusd_contract.exchange = 'IDEALPRO'
eurusd_contract.currency = 'CNH'

#Request Market Data
app.reqMktData(1, eurusd_contract, '', False, False, [])

time.sleep(3) #Sleep interval to allow time for incoming price data
app.disconnect()