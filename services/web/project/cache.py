import redis
import json
from pprint import pprint
import redis_lock
from time import sleep 
from datetime import datetime
import threading
from dataclasses import dataclass
from math import log
from random import random
import psycopg2
import signal

q = """select t.category, t.city, t.rent_time from 
	(select c3."name" as category, c2.city, sum(r.return_date - r.rental_date) as rent_time, rank() over (partition by c2.city order by sum(r.return_date - r.rental_date) desc) as rnk from rental r 
	join customer c on c.customer_id = r.customer_id 
	join address a on a.address_id = c.customer_id 
	join city c2 on c2.city_id = a.city_id 
	join inventory i on i.inventory_id = r.inventory_id 
	join film_category fc on fc.film_id = i.film_id 
	join category c3 on c3.category_id = fc.category_id 
	where r.return_date is not null and r.rental_date is not NULL
	group  by c2.city, category) t
where t.rnk = 1 and (lower(t.city) like 'a%' or t.city like '%-%');"""

def load_from_db(request: str):
    print('recalc')
    ret = {}
    conn = psycopg2.connect(database="pagila", user="hello_flask", password="hello_flask", host="localhost", port=5432)
    try:
        with conn.cursor() as cur:
            cur.execute(q)
            all = cur.fetchall()
            ret = dict.fromkeys(range(len(all)), all)
    finally:
        conn.close()

    return ret

def recalc(request: str, ttl: int, conn: redis.Redis):
    lock = redis_lock.Lock(conn, request)
    if lock.acquire(blocking=False):
        print('from db')
        try:
            t = datetime.now()
            data = load_from_db(request)
            ct = str((datetime.now()-t).total_seconds())
            conn.hset(request, 'data', data)
            conn.hset(request, 'ct', str(ct))
            conn.expire(request, ttl)
            lock.release()
            return json.loads(data)
        except Exception as e:
            print(e)
            lock.release()
    return None

def get_data(request: str, ttl: int, conn: redis.Redis):
    data = conn.hget(request, 'data')
    if data:
        print('from cache |', conn.ttl(request), '|', float(conn.hget(request, 'ct')))
        return json.loads(data)
    else:
        r = recalc(request, ttl, conn)
        if r:
            return r
        else:
            print('wait lock')
            for _ in range(20):
                sleep(0.5)
                data = conn.hget(request, 'data')
                if data:
                    return json.loads(data)
            #timeout
            print('lock timeout')
            return get_data(request, ttl, conn)


class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True

def cache_updater(conn: redis.Redis):
    beta = 1.0
    conn = redis.Redis(host = 'localhost', port = 6379, db = 1)
    killer = GracefulKiller()
    while not killer.kill_now:
        sleep(1)
        keys = conn.keys(pattern='*')
        for key in keys:
            if key.startswith(b'lock'):
                continue
            ct = conn.hget(key, 'ct')
            if ct == None:
                continue
            computeTime = float(ct)
            ttl = conn.ttl(key)
            p = beta - log(random()) * computeTime
            print(key, '|', p, '>', ttl, ':', p>ttl)
            if p > ttl:
                r = threading.Thread(name='recalc', target=lambda: recalc(key.decode("utf-8", "ignore"), 10, conn))
                r.start()


def run_cache_updater():
    b = threading.Thread(name='cache_updater', target=cache_updater)
    b.start()


if __name__ == '__main__':
    cache_updater()
