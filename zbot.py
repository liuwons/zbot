import zapi
import json


def scale(num, sc):
    return float(int(num * pow(10, sc))) / pow(10, sc)


class P10Sell:
    def __init__(self, api, market, init, profit=0.01, diff=0.01):
        self._api_ = api
        self._market_ = market
        self._init_ = init
        self._amount_scale_ = 2
        self._price_scale_ = 2
        self._orders_ = []
        self._profit_ = profit
        self._diff_ = diff

    def start(self):
        coin = self._market_.split('_')[0]
        account = self._api_.get_account_info()
        for c in account['result']['coins']:
            if c['key'] == coin:
                coin_amount = c['available']
                print coin, ' amount: ', coin_amount
                if coin_amount < self._init_:
                    print 'Error: coin amount not enougn'
                    return
        markets = self._api_.markets()
        if self._market_ not in markets:
            print 'get market ', self._market_, ' failed'
            return
        self._amount_scale_ = markets[self._market_]['amountScale']
        self._price_scale_ = markets[self._market_]['priceScale']
        print 'amount scale: ', self._amount_scale_
        print 'price scale: ', self._price_scale_
        cur_price = float(self._api_.ticker(self._market_)['ticker']['last'])
        print 'current price: ', cur_price
        total = self._init_
        last_price = cur_price * 0.995
        order_count = 10
        while total > 0:
            if order_count < 0:
                break
            price = scale(last_price * (1+self._diff_), self._price_scale_)
            if price <= last_price:
                break
            amount = total / 10.0
            amount = scale(amount, self._amount_scale_)
            if amount < 0.00001:
                break
            total -= amount
            order_result = self._api_.order(self._market_, zapi.ORDER_TYPE_SELL, amount, price)
            if order_result['code'] == '1000' or order_result['code'] == 1000:
                order_id = order_result['id']
                print order_id, ' : sell ', amount, coin, ' at price ', price
                self._orders_ += [order_id]
                last_price = price
                order_count -= 1
            else:
                print 'Error: failed to sell ', amount, coin, ' at price ', price, ' errcode: ', order_result['code']
        self.loop()

    def loop(self):
        print 'start loop'
        while True:
            for order in self._orders_:
                detail = self._api_.get_order(self._market_, str(order))
                stat = detail['status']
                if stat == zapi.ORDER_STATUS_DONE:
                    print order, ' done'
                    order_type = detail['type']
                    trade_amount = detail['trade_amount']
                    trade_price = detail['price']
                    trade_money = float(str(detail['trade_money'])) # sell
                    if order_type == zapi.ORDER_TYPE_BUY:
                        price = scale((1 + self._profit_) * trade_price, self._price_scale_)
                        order_result = self._api_.order(self._market_, zapi.ORDER_TYPE_SELL, trade_amount, price)
                        if order_result['code'] == '1000' or order_result['code'] == 1000:
                            order_id = order_result['id']
                            print order_id, ' : sell ', trade_amount, ' at price ', price
                            self._orders_ += [order_id]
                        else:
                            print 'failed to sell ', trade_amount, ' at price ', price
                    else:
                        price = scale((1 - self._profit_) * trade_price, self._price_scale_)
                        amount = scale(trade_money / price, self._amount_scale_)
                        order_result = self._api_.order(self._market_, zapi.ORDER_TYPE_BUY, amount, price)
                        if order_result['code'] == '1000' or order_result['code'] == 1000:
                            order_id = order_result['id']
                            print order_id, ' : buy ', amount, ' at price ', price
                            self._orders_ += [order_id]
                        else:
                            print 'failed to buy ', trade_amount, ' at price ', price
                    self._orders_.remove(order)
                    break


def main():
    conf = json.load(open('conf.json'))
    if 'zb' not in conf:
        print 'configure file error, read zb failed'
        return
    if 'access_key' not in conf['zb']:
        print 'configure file error, read access_key failed'
        return
    if 'secret_key' not in conf['zb']:
        print 'configure file error, read secret_key failed'
        return
    access_key = conf['zb']['access_key']
    secret_key = conf['zb']['secret_key']

    zpi = zapi.ZApi(str(access_key), str(secret_key))
    if 'trades' not in conf['zb']:
        print 'no trade specific'
        return
    trades = conf['zb']['trades']
    for trade in trades:
        if trade['strategy'] == 'P10Sell':
            bot = P10Sell(zpi, str(trade['market']), trade['init'])
            bot.start()


if __name__ == '__main__':
    main()
