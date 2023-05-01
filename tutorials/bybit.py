import json
import requests
import time
import hashlib
import hmac
import uuid


class Bybit:
    def __init__(self):
        self.httpClient = requests.Session()
        self.recv_window = str(10000)
        self.url = "https://api.bybit.com"

    def HTTP_Request(self, api_key, api_secret, endPoint, method, payload, Info):
        global time_stamp
        time_stamp = str(int(time.time() * 10 ** 3))
        print(time_stamp)
        print(self.recv_window)
        signature = self.genSignature(api_key, api_secret, payload=payload)
        headers = {
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': self.recv_window,
            'Content-Type': 'application/json'
        }
        if method == "POST":
            response = self.httpClient.request(method, self.url + endPoint, headers=headers, data=payload)
        else:
            response = self.httpClient.request(method, self.url + endPoint + "?" + payload, headers=headers)
        print(response.text)
        print(Info + " Elapsed Time : " + str(response.elapsed))
        return response




    def genSignature(self, api_key, api_secret, payload):
        param_str = str(time_stamp) + api_key + self.recv_window + payload
        hash = hmac.new(bytes(api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature

    def updateTPOrderLong(self, api_key, api_secret, symbol, take_profit):
        take_profit = str(take_profit)

        endpoint = "/contract/v3/private/position/trading-stop"
        method = "POST"
        params = '{"symbol":"' + symbol + '","takeProfit":"' + take_profit + '","positionIdx": "0"}'
        print(params)
        return self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create").json()

    def updateTPOrderShort(self, api_key, api_secret, symbol, take_profit):
        take_profit = str(take_profit)

        endpoint = "/contract/v3/private/position/trading-stop"
        method = "POST"
        params = '{"symbol":"' + symbol + '","takeProfit":"' + take_profit + '","positionIdx": "0"}'
        print(params)
        return self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create").json()

    def updateSLOrder(self, api_key, api_secret, symbol, stop_loss):
        stop_loss = str(stop_loss)

        endpoint = "/contract/v3/private/position/trading-stop"
        method = "POST"
        params = '{"symbol":"' + symbol + '","stopLoss":"' + stop_loss + '","positionIdx": "0"}'
        print(params)
        response = self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create")

        return response.json()

    def cancelOrder(self, api_key, api_secret, symbol, orderId):
        orderId = str(orderId)

        endpoint = "/contract/v3/private/order/cancel"
        method = "POST"
        params = '{"symbol":"' + symbol + '","orderId": ' + orderId + '"}'
        print(params)
        return self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create").json()

    def cancelAllOrders(self, api_key, api_secret, symbol):

        endpoint = "/contract/v3/private/order/cancel-all"
        method = "POST"
        params = '{"symbol":"' + symbol + '"}'
        print(params)
        return self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create").json()

    def long(self, api_key, api_secret, symbol, qty, price, take_profit, stop_loss):
        qty = str(qty)
        symbol = str(symbol)
        price = str(price)
        take_profit = str(take_profit)
        stop_loss = str(stop_loss)

        endpoint = "/contract/v3/private/order/create"
        method = "POST"
        orderLinkId = uuid.uuid4().hex
        params = '{' \
                 '"symbol": "'+symbol+'",' \
                 '"side": "Buy",' \
                                      '"positionIdx": "0",' \
                 '"orderType": "Limit",' \
                 '"qty": "'+qty+'",' \
                 '"price": "'+price+'",' \
                 '"is_isolated": false,' \
                 '"tpTriggerBy": "MarkPrice",' \
                 '"slTriggerBy": "MarkPrice",' \
                 '"triggerBy": "MarkPrice",' \
                 '"triggerDirection": 2,' \
                 '"timeInForce": "GoodTillCancel",' \
                 '"orderLinkId": "'+orderLinkId+'",' \
                 '"takeProfit": "'+take_profit+'",' \
                 '"stopLoss": "'+stop_loss+'",' \
                 '"reduce_only": false,' \
                 '"closeOnTrigger": false' \
                 '}'
        print(params)
        return self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create").json()

    def short(self, api_key, api_secret, symbol, qty, price, take_profit, stop_loss):
        qty = str(qty)
        price = str(price)
        take_profit = str(take_profit)
        stop_loss = str(stop_loss)

        endpoint = "/contract/v3/private/order/create"
        method = "POST"
        orderLinkId = uuid.uuid4().hex
        params = '{' \
                 '"symbol": "' + symbol + '",' \
                '"side": "Sell",' \
                 '"is_isolated": false,' \
                                          '"positionIdx": "0",' \
                                          '"orderType": "Limit",' \
                                          '"qty": "' + qty + '",' \
                                                             '"price": "' + price + '",' \
                                                                                                                  '"tpTriggerBy": "MarkPrice",' \
                                                                                                                  '"slTriggerBy": "MarkPrice",' \
                                                                                                                  '"triggerBy": "MarkPrice",' \
                                                                                                                  '"triggerDirection": 1,' \
                                                                                                                  '"timeInForce": "GoodTillCancel",' \
                                                                                                                  '"orderLinkId": "' + orderLinkId + '",' \
                                                                                                                                                     '"takeProfit": "' + take_profit + '",' \
                                                                                                                                                                                       '"stopLoss": "' + stop_loss + '",' \
                                                                                                                                                                                                                     '"reduce_only": false,' \
                                                                                                                                                                                                                     '"closeOnTrigger": false' \
                                                                                                                                                                                                                     '}'
        print(params)
        return self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create").json()

    def buy(self, api_key, api_secret, symbol, qty, price):
        qty = str(qty)
        price = str(price)
        endpoint = "/spot/v3/private/order"
        method = "POST"
        orderLinkId = uuid.uuid4().hex
        params = '{"symbol":"' + symbol + '","orderType":"Limit","side":"Buy","orderLinkId":"' + orderLinkId + '","orderQty":"' + qty + '","orderPrice":"' + price + '","timeInForce":"GTC"}'
        print(self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create"))

    def sell(self, api_key, api_secret, symbol, qty, price):
        qty = str(qty)
        price = str(price)
        endpoint = "/spot/v3/private/order"
        method = "POST"
        orderLinkId = uuid.uuid4().hex
        params = '{"symbol":"' + symbol + '","orderType":"Limit","side":"Sell","orderLinkId":"' + orderLinkId + '","orderQty":"' + qty + '","orderPrice":"' + price + '","timeInForce":"GTC"}'
        print(self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create"))

    def available_balance(self, api_key, api_secret, coin):
        endpoint = "/contract/v3/private/account/wallet/balance"
        method = "GET"
        params = 'coin=' + coin
        json_resp = self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create").json()
        available = float(json_resp["result"]["list"][0]["availableBalance"])
        return available

    def set_leverage(self, api_key, api_secret, symbol, leverage):
        leverage = str(leverage)

        endpoint = "/contract/v3/private/position/set-leverage"
        method = "POST"
        params = '{"symbol":"' + symbol + '","buyLeverage": "' + leverage + '","sellLeverage": "'+ leverage + '"}'
        print(params)
        response = self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create")
        return response
        #return self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create").json()

    def setOneWay(self, api_key, api_secret, symbol):
        mode = "0"

        endpoint = "/contract/v3/private/position/switch-mode"
        method = "POST"
        params = '{"symbol":"' + symbol + '","mode": ' + mode + '}'
        print(params)
        response = self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create")
        return response
        #return self.HTTP_Request(api_key, api_secret, endpoint, method, params, "Create").json()
