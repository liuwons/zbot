import zapi
import json
import time
import logging


logging.basicConfig(level=logging.DEBUG)


def scale(num, sc):
    return float(int(num * pow(10, sc))) / pow(10, sc)


class P10Sell:
    def __init__(self, bot_name, api, market, init, profit=0.01, diff=0.01, orders='P10Sell_orders.json'):
        self._api_ = api
        self._market_ = market
        self._init_ = init
        self._amount_scale_ = 2
        self._price_scale_ = 2
        self._orders_ = []
        self._profit_ = profit
        self._diff_ = diff
        self._name_ = bot_name
        self._order_fname_ = orders

        self._logger_ = logging.getLogger(name=self._name_)
        handler = logging.FileHandler(self._name_ + '.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        self._logger_.addHandler(handler)

    def init_orders(self):
        try:
            js = json.load(open(self._order_fname_))
            print 'get order: '
            print js
            self._orders_ = js
            self._logger_.info('load ' + str(len(self._orders_)) + ' orders from ' + self._order_fname_)
            return
        except Exception, e:
            print e

        coin = self._market_.split('_')[0]
        cur_price = float(self._api_.ticker(self._market_)['ticker']['last'])
        self._logger_.info('current price: ' + str(cur_price))
        total = self._init_
        last_price = cur_price * 0.995
        order_count = 10
        while total > 0:
            if order_count < 0:
                break
            price = scale(last_price * (1 + self._diff_), self._price_scale_)
            if price <= last_price:
                break
            amount = total / 10.0
            amount = scale(amount, self._amount_scale_)
            if amount < 0.00001:
                break
            total -= amount
            order_result = self._api_.order(self._market_, zapi.ORDER_TYPE_SELL, amount, price)
            if order_result['code'] == '1000' or order_result['code'] == 1000:
                order_id = str(order_result['id'])
                self._logger_.info(order_id + ' : sell ' + str(amount) + coin + ' at price ' + str(price))
                self._orders_ += [order_id]
                last_price = price
                order_count -= 1
            else:
                self._logger_.error('failed to sell ' + str(amount) + coin + ' at price ' + str(price) + ' errcode: ' + order_result['code'])

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
            print 'Error: get market ', self._market_, ' failed'
            return
        self._amount_scale_ = markets[self._market_]['amountScale']
        self._price_scale_ = markets[self._market_]['priceScale']
        self._logger_.info('amount scale: ' + str(self._amount_scale_))
        self._logger_.info('price scale: ' + str(self._price_scale_))

        self.init_orders()

        self.loop()

    def loop(self):
        self._logger_.info('start loop')
        with open(self._order_fname_, 'w') as f:
            json.dump(self._orders_, f)
        while True:
            time.sleep(0.5)
            for order in self._orders_:
                detail = self._api_.get_order(self._market_, str(order))
                stat = detail['status']
                if stat == zapi.ORDER_STATUS_DONE:
                    self._logger_.info(str(order) + ' done')
                    order_type = detail['type']
                    trade_amount = detail['trade_amount']
                    trade_price = detail['price']
                    trade_money = float(str(detail['trade_money'])) # sell
                    if order_type == zapi.ORDER_TYPE_BUY:
                        price = scale((1 + self._profit_) * trade_price, self._price_scale_)
                        order_result = self._api_.order(self._market_, zapi.ORDER_TYPE_SELL, trade_amount, price)
                        if order_result['code'] == '1000' or order_result['code'] == 1000:
                            order_id = order_result['id']
                            self._logger_.info(str(order_id) + ' : sell ' + str(trade_amount) + ' at price ' + str(price))
                            self._orders_ += [order_id]
                        else:
                            self._logger_.error('failed to sell ' + str(trade_amount) + ' at price ' + str(price))
                    else:
                        price = scale((1 - self._profit_) * trade_price, self._price_scale_)
                        amount = scale(trade_money / price, self._amount_scale_)
                        order_result = self._api_.order(self._market_, zapi.ORDER_TYPE_BUY, amount, price)
                        if order_result['code'] == '1000' or order_result['code'] == 1000:
                            order_id = order_result['id']
                            self._logger_.info(str(order_id) + ' : buy ' + str(amount) + ' at price ' + str(price))
                            self._orders_ += [order_id]
                        else:
                            self._logger_.error('failed to buy ' + str(trade_amount) + ' at price ' + str(price))
                    self._orders_.remove(order)
                    with open(self._order_fname_, 'w') as f:
                        json.dump(self._orders_, f)
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
            bot = P10Sell("P10Sell", zpi, str(trade['market']), trade['init'])
            bot.start()


if __name__ == '__main__':
    main()
