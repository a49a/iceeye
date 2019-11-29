from functools import partial
import traceback

from requests import Session

import gevent
from gevent import monkey
from gevent.pool import Pool

# Monkey-patch.
monkey.patch_all(thread=False, select=False)


class Areq():

    def __init__(self, method, url, **kwargs):
        self.method = method
        self.url = url
        self.session = Session()
        self.response = None

    def send(self, **kwargs):
        try:
            self.response = self.session.request(self.method, self.url, **kwargs)
        except Exception as e:
            self.exception = e
            self.traceback = traceback.format_exc()


get = partial(Areq, "GET")


# load request job
def load(r, pool=None, stream=False):
    if pool is not None:
        return pool.spawn(r.send, stream=stream)
    return gevent.spawn(r.send, stream=stream)


# synonym
def request(method, url, **kwargs):
    return Areq(method, url, **kwargs)


def map(reqs, size=None, exception_handler=None, gtimeout=None):
    pool = Pool(size) if size else None
    jobs = [load(r, pool) for r in reqs]
    gevent.joinall(jobs, timeout=gtimeout)

    ret = []

    for req in reqs:
        if req.response is not None:
            ret.append(req.response)
        elif exception_handler and hasattr(req, 'exception'):
            ret.append(exception_handler(req, req.exception))
        else:
            ret.append(None)

    return ret


def imap(reqs, stream=False, size=2, exception_handler=None):
    pool = Pool(size)
    # TODO 返回迭代器功能


    pass
