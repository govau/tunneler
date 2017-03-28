
from tunneler.command import parse_args


def test_args():
    args = parse_args(['task_name', 'connection_name'])
    assert args.task_name == 'task_name'
    assert args.connection_name == 'connection_name'
