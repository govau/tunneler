from __future__ import unicode_literals

import os
import errno


def parts(dburl):
    before, remainder = dburl.split('@', 1)
    host, path = remainder.split('/', 1)
    host = host.split(':')[0]
    return before, host, path


def host_from_dburl(dburl):
    _, host, _ = parts(dburl)
    return host


def local_dburl(dburl, port):
    before, host, path = parts(dburl)
    return before + '@' + '127.0.0.1:' + str(port) + '/' + path


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
