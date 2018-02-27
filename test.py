import json
import zapi


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

    # print zpi.markets()
    # print zpi.ticker("btc_qc")
    # print zpi.depth("btc_qc", 2)
    # print zpi.trades("btc_qc")
    # print zpi.kline("btc_qc")

    # print zpi.order('zb_qc', zapi.ORDER_TYPE_BUY, '100', '5.0008')
    # print zpi.cancel_order('zb_qc', '2018022615327073')
    print zpi.get_order('zb_qc', '2018022715770615')
    # print zpi.get_orders('zb_qc', '1', zapi.ORDER_TYPE_BUY)
    # print zpi.get_orders_new('zb_qc', '1', '20', zapi.ORDER_TYPE_BUY)
    # print zpi.get_orders_ignore_tader_type('zb_qc', '1', '10')
    # print zpi.get_unfinished_orders_ignore_trade_type('zb_qc', '1', '10')
    # print zpi.get_account_info()
    # print zpi.get_user_address('ltc')
    # print zpi.get_withdraw_address('ltc')
    # print zpi.get_withdraw_record('ltc', '1', '10')
    # print zpi.get_charge_record('ltc', '1', '10')

if __name__ == '__main__':
    main()
