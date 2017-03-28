from __future__ import absolute_import


import sys
import argparse
import os

from sqlbag import S


from .connect import connection_from_connection_name


def run(args):
    if args.connection_name:
        os.environ['TUNNELER_CONNECTION'] = args.connection_name

    try:
        import tasks
    except ImportError:
        import tunneler.tasks as tasks

    task_method = getattr(tasks, args.task_name)

    with connection_from_connection_name(args.connection_name) as REAL_DB_URL:
        print('connecting to: {}'.format(REAL_DB_URL))

        with S(REAL_DB_URL, echo=False) as s:
            s.execute('select 1')

        print('connection successful.')

        task_method(REAL_DB_URL)
        print('task complete, closing connection.')


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Open a connection and run a task.')

    parser.add_argument(
        'task_name',
        help='')

    parser.add_argument(
        'connection_name',
        help='')

    return parser.parse_args(args)


def do_command():  # pragma: no cover
    args = parse_args(sys.argv[1:])
    status = run(args)
    sys.exit(status)
