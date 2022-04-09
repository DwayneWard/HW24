import re
from typing import Iterator


def run_command(iter_obj: Iterator, query: str) -> Iterator:
    query_items = query.split('|')
    result = iter(map(lambda v: v.strip(), iter_obj))
    for item in query_items:
        cmd_value = item.split(':')
        command = cmd_value[0]
        value = cmd_value[1]
        result = get_data_by_cmd(result, command, value)
    return result


def get_data_by_cmd(iter_obj: Iterator, command: str, value: str) -> Iterator:
    if command == "filter":
        return filter(lambda v: value in v, iter_obj)
    if command == 'map':
        return map(lambda v: v.split(" ")[int(value)], iter_obj)
    if command == 'unique':
        return iter(set(iter_obj))
    if command == 'sort':
        order = value
        if order == 'desc':
            return iter(sorted(iter_obj, reverse=True))
        else:
            return iter(sorted(iter_obj))
    if command == 'limit':
        return get_limit(iter_obj, int(value))
    if command == 'regex':
        regex = re.compile(value)
        return filter(lambda v: regex.search(v), iter_obj)
    return iter_obj

def get_limit(iter_obj: Iterator, value: int) -> Iterator:
    i = 0
    for item in iter_obj:
        if i < value:
            yield item
        else:
            break
        i += 1
