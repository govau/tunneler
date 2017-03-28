from __future__ import unicode_literals

import io
import os
import yaml
from contextlib import contextmanager

import six
import paramiko
from sshtunnel import SSHTunnelForwarder

from .util import host_from_dburl, local_dburl


SSH_CONFIG_FILE = '~/.ssh/config'


def get_ssh_config(ssh_name):
    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser(SSH_CONFIG_FILE)

    with io.open(user_config_file) as f:
        ssh_config.parse(f)

    cfg = {}

    user_config = ssh_config.lookup(ssh_name)

    for k in ('hostname', 'user', 'port', 'identityfile'):
        if k in user_config:
            cfg[k] = user_config[k]
    cfg['ssh_username'] = cfg.pop('user', None)
    cfg['remote_host'] = cfg.pop('hostname', None)
    cfg['remote_port'] = cfg.pop('port', None)

    if cfg['identityfile']:
        with io.open(cfg['identityfile'][0]) as f:
            cfg['ssh_pkey'] = f.read()
        del cfg['identityfile']

    cfg = {k: v for k, v in cfg.items() if v}
    return cfg


def get_config(filename='connections.yaml'):
    with io.open(filename) as f:
        config = yaml.load(f.read())

    for k, values in config.items():
        if 'ssh_config' in values:
            ssh_config = get_ssh_config(values['ssh_config'])
            config_from_file = config[k]
            del config_from_file['ssh_config']
            ssh_config.update(config_from_file)
            config[k] = ssh_config
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
