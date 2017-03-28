from __future__ import unicode_literals

import io
import yaml
from contextlib import contextmanager

import six
import paramiko
from sshtunnel import SSHTunnelForwarder

from .util import host_from_dburl, local_dburl


def get_config(filename='connections.yaml'):
    with io.open(filename) as f:
        config = yaml.load(f.read())
    return config


@contextmanager
def connection_from_connection_name(connection_name):
    config = get_config()
    settings = config[connection_name]

    with connection_from_settings(**settings) as dburl:
        yield dburl


@contextmanager
def connection_from_settings(
        ssh_username,
        ssh_pkey,
        local_port,
        remote_host,
        private_dburl,
        private_port=5432,
        remote_port=22):

    pk = paramiko.RSAKey.from_private_key(
        file_obj=io.StringIO(six.text_type(ssh_pkey))
    )

    private_host = host_from_dburl(private_dburl)
    connection_url = local_dburl(private_dburl, local_port)

    with SSHTunnelForwarder(
        (remote_host, remote_port),
        ssh_username=ssh_username,
        ssh_pkey=pk,
        remote_bind_address=(private_host, private_port),
        local_bind_address=('0.0.0.0', local_port)
    ):
        yield connection_url
