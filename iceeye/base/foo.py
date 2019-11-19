from bs4 import BeautifulSoup
from gevent import monkey, pool
monkey.patch_all()
import gevent
import requests


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) " +
                  "AppleWebKit/537.36 (KHTML, like Gecko) " +
                  "Chrome/58.0.3029.110 Safari/537.36"
}

r = requests.get('https://www.baidu.com', headers=headers)


def req(i):
    r = requests.get('https://www.baidu.com', headers=headers)
    # soup = BeautifulSoup(r.text, features='lxml')
    print(i, r)


def con_req(concurrency):
    req_pool = pool.Pool(concurrency)
    req_pool.map(req, range(15))


con_req(5)
