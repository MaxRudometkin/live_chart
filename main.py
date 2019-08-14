"""
this file will keep last hour trade history in database
query exchange API every 1 second and update database

"""
import os

import yaml
import time
import ccxt
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db_classes import BASE, TradeHistoryLive


def get_last_price(market):
    # get last price
    try:
        response = exchange.fetch_ticker(market)

        # convert str datetime to datetime object
        format = "%Y-%m-%dT%H:%M:%S.%fZ"
        response['datetime'] = datetime.strptime(response['datetime'], format)


    except Exception as err:
        print(err)
        return None

    return response


def db_add_new_row(exchange_response):
    # add new row in database

    session.add(TradeHistoryLive(date=exchange_response['datetime'],
                                 exchange=exchange.name,
                                 market=exchange_response['symbol'],
                                 last=exchange_response['last']))

    print('{} {} new row added'.format(exchange_response['symbol'],
                                       exchange_response['datetime']))


def update_db_row(exchange_response, db_response):
    db_response.date = exchange_response['datetime']
    db_response.last = exchange_response['last']

    print('{} row updated'.format(exchange_response['symbol'],
                                  exchange_response['datetime']))


def update_database(exchange_response):
    if exchange_response is None:
        return

    # get current database data
    db_response = session.query(TradeHistoryLive) \
        .filter(TradeHistoryLive.exchange == exchange.name) \
        .filter(TradeHistoryLive.market == exchange_response['symbol']) \
        .order_by(TradeHistoryLive.date.desc()) \
        .limit(5)

    if not db_response.count():
        # add new data to db
        db_add_new_row(exchange_response)


    # for r in db_response:
    #     print(r.date)

    else:
        # get last update from db
        last_update = db_response[0].date
        last_update = last_update.replace(second=0, microsecond=0)
        last_update = last_update + timedelta(minutes=1)

        # print('\n')
        # print("new data: {}".format(exchange_response['datetime']))
        # print("db data: {}".format(db_response[0].date))
        # print('\n')

        # if same minute
        if exchange_response['datetime'] < last_update:
            # update db
            update_db_row(exchange_response, db_response[0])
        else:
            # new row
            db_add_new_row(exchange_response)

    # commit db
    session.commit()
    print('{} {} done'.format(exchange_response['datetime'],
                              exchange_response['symbol']))


def delete_old_data():
    """
    delete all data that older than 1 hour
    """

    date = datetime.now() - timedelta(hours=1)
    session.query(TradeHistoryLive).filter(TradeHistoryLive.date < date).delete()
    session.commit()


def main():
    """ main loop"""
    while True:
        for market in config['markets']:
            # get last price
            response = get_last_price(market)
            # update database
            update_database(response)
            # delete old db data
            delete_old_data()
            # sleep
            time.sleep(config['time_sleep'])


if __name__ == '__main__':
    # read config file
    with open('config.yaml', 'r') as yaml_file:
        config = yaml.load(yaml_file)

    print('read config - done')

    # database connection
    engine = create_engine(os.environ['DATABASE_URL'])
    BASE.metadata.create_all(engine, checkfirst=True)
    session = sessionmaker(bind=engine)()

    print('db connection - done')

    # create exchange
    exchange = ccxt.bitmex({
        'apiKey': '',
        'secret': '',
    })

    main()
