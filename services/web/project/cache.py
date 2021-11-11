import redis
import json
from pprint import pprint
import redis_lock
from time import sleep 
from datetime import datetime
import threading
from dataclasses import dataclass
from math import log, ceil
from random import random
import psycopg2
import signal
import hashlib

def request2key(request: str):
    return 'q:'+hashlib.sha1(str.encode('utf-8')).hexdigest()

def load_from_db(request: str):
    print('recalc', flush=True)
    ret = {}
    conn = None
    try:
        conn = psycopg2.connect(database="pagila", user="hello_flask", password="hello_flask", host="db", port=5432)
        with conn.cursor() as cur:
            cur.execute(request)
            all = cur.fetchall()
            ret = dict.fromkeys(range(len(all)), all)
    finally:
        if conn:
            conn.close()

    return ret

def recalc(request: str, ttl: int, conn: redis.Redis):
    data_key = request2key(request)
    lock = redis_lock.Lock(conn, data_key)
    if lock.acquire(blocking=False):
        print('from db', flush=True)
        try:
            t = datetime.now()
            data = load_from_db(request)
            ct = str(ceil((datetime.now()-t).total_seconds()))
            conn.hset(data_key, 'data', json.dumps(data))
            conn.hset(data_key, 'ct', str(ct))
            conn.hset(data_key, 'q', request)
            conn.expire(data_key, ttl)
            lock.release()
            return data
        except Exception as e:
            print(e, flush=True)
            lock.release()
    return None


def get_data(request: str, ttl: int, conn: redis.Redis):
    beta = 1.0
    data_key = request2key(request)
    data = conn.hget(data_key, 'data')
    if data:
        print('from cache |', conn.ttl(data_key), '|', float(conn.hget(data_key, 'ct')), flush=True)
        
        computeTime = float(conn.hget(data_key, 'ct'))
        ttl = conn.ttl(data_key)
        
        if ceil(beta * (- log(random())) * computeTime) > ttl:
            r = threading.Thread(name='recalc', target=lambda: recalc(request, ttl, conn))
            r.start()
        return json.loads(data)
    else:
        data = recalc(request, ttl, conn)
        if data:
            return data
        else:
            print('wait lock', flush=True)
            for _ in range(20):
                sleep(0.5)
                data = conn.hget(data_key, 'data')
                if data:
                    return json.loads(data)
            #timeout
            print('lock timeout', flush=True)
            return get_data(request, ttl, conn)


def get_data_x(request: str, ttl: int, conn: redis.Redis):
    data_key = request2key(request)
    data = conn.hget(data_key, 'data')
    if data:
        print('from cache |', conn.ttl(data_key), '|', conn.hget(data_key, 'ct'), flush=True)
        return json.loads(data)
    else:
        r = recalc(request, ttl, conn)
        if r:
            return r
        else:
            print('wait lock', flush=True)
            for _ in range(20):
                sleep(0.5)
                data = conn.hget(data_key, 'data')
                if data:
                    return json.loads(data)
            #timeout
            print('lock timeout', flush=True)
            return get_data_x(request, ttl, conn)


class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True

def cache_updater(expire: int):
    beta = 1.0
    conn = redis.Redis(host = 'redis', port = 6379, db = 1)
    killer = GracefulKiller()
    while not killer.kill_now:
        sleep(1)
        keys = conn.keys(pattern='q:*')
        for key in keys:
            if not key.startswith(b'q:'):
                continue
            ct = conn.hget(key, 'ct')
            if ct == None:
                continue
            q = conn.hget(key, 'q')
            if q == None:
                continue
            computeTime = float(ct)
            ttl = conn.ttl(key)
            p = ceil(beta * (- log(random())) * computeTime)
            print(key, '|', p, '>', ttl, ':', p>ttl, flush=True)
            if p > ttl:
                r = threading.Thread(name='recalc', target=lambda: recalc(q.decode("utf-8", "ignore"), expire, conn))
                r.start()


def run_cache_updater():
    b = threading.Thread(name='cache_updater', target=cache_updater)
    b.start()


if __name__ == '__main__':
    cache_updater(30)
