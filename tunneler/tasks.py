from __future__ import unicode_literals, print_function


import subprocess
import os

from sqlbag import S


from .util import mkdir_p


def test_connection(dburl):
    with S(dburl, echo=True) as s:
        s.execute('select 1')


def _do_pg_dump(dburl, schema_only=False):
    schema_flag = '--schema-only' if schema_only else ''
    schema_fname = '.schema' if schema_only else '.full'

    COMMAND = 'pg_dump --no-owner --no-privileges {} --column-inserts -f {} {}'

    output_file = 'dumps/{}{}.dump.sql'.format(
        os.environ.get('TUNNELER_CONNECTION'),
        schema_fname
    )

    command = COMMAND.format(schema_flag, output_file, dburl)
    print('RUNNING: {}'.format(command))

    mkdir_p('dumps')
    output = subprocess.check_output(command, shell=True)
    print(output)


def do_full_pg_dump(dburl):
    _do_pg_dump(dburl)


def do_schema_pg_dump(dburl):
    _do_pg_dump(dburl, schema_only=True)
