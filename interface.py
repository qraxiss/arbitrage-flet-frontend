from config import API_URI
from requests import get, patch, post


def get_token(address=None):
    return get(f'{API_URI}/tokens', json={
        "address": address
    }).json()


def set_token_track(address, track):
    X = patch(f'{API_URI}/tokens', json={
        "address": address,
        "track": track
    })

    return X


def add_token(token):
    return post(f'{API_URI}/tokens', json=token).json()


def get_pool(swap=None, fee=None, version=None, t1=None):
    return get(f'{API_URI}/pools', json={
        "swap": swap,
        "fee": fee,
        "version": version,
        "t1": t1,
    }
    ).json()


def update_price(swap, fee, version, t1, side, price):
    return patch(f'{API_URI}/pools', json={
        "swap": swap,
        "fee": fee,
        "version": version,
        "t1": t1,
        "side": side,
        "price": price
    }).json()


def update_volume(swap, fee, version, t1, volume):
    return patch(f'{API_URI}/pools', json={
        "swap": swap,
        "fee": fee,
        "version": version,
        "t1": t1,
        "side": "volume",
        "price": volume
    }).json()

def add_pool(pool):
    return post(f'{API_URI}/pools', json=pool).json()


def get_best_prices():
    return get(f'{API_URI}/best_prices').json()


def open_pair(address):
    return set_token_track(address, True)

def close_pair(address):
    return set_token_track(address, False)

def open_all_tokens():
    for token in get_token():
        open_pair(token['address'])

def close_all_tokens():
    for token in get_token():
        close_pair(token['address'])

def open_pool(swap, fee, version, t1):
    return update_volume(swap, fee, version, t1, True)

def close_pool(swap, fee, version, t1):
    return update_volume(swap, fee, version, t1, False)

def open_all_pools():
    for pool in get_pool():
        open_pool(**pool)

def close_all_pools():
    for pool in get_pool():
        close_pool(**pool)


def get_binance_prices():
    return get(f'{API_URI}/binance').json()


def get_trades():
    return get(f'{API_URI}/trades').json()