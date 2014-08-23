#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick n dirty CLI for checking ec2 inventory

Specifically design for my own personal workflow.
"""
import sys

from boto import ec2
from tabulate import tabulate


HEADERS = (
    'name',
    'environment',
    'site',
    'ip',
    'private_ip',
    'launch_time',
    'id',
)


def to_row(instance):
    """Format data about the instance to be printed."""
    # WISHLIST use `sort_key` and `HEADERS` to be DRY?
    return (
        instance.tags.get('Name'),
        instance.tags.get('environment'),
        instance.tags.get('site'),
        instance.ip_address, instance.private_ip_address,
        instance.launch_time.split('T', 2)[0],
        instance.id,
    )


def sort_key(key):
    """Get the accessor function for an instance to look for `key`."""
    # look for tags that match
    if key == 'name':
        return lambda x: x.tags.get('Name')
    if key in ('environment', 'site'):
        return lambda x: x.tags.get(key)
    # look for attributes that match
    return lambda x: getattr(x, key)


def filter_key(filter_args):
    def filter_instance(instance):
        return all([value == sort_key(key)(instance)
            for key, value in filter_args.items()])
    return filter_instance


def voyeur(sort_by=None, filter_by=None):
    conn = ec2.connect_to_region('us-east-1')  # XXX magic constant

    instances = conn.get_only_instances()

    if sort_by:
        instances.sort(key=sort_key(sort_by))
    if filter_by:
        instances = filter(filter_key(filter_by), instances)  # XXX overwriting original

    print tabulate(map(to_row, instances), headers=HEADERS)


def list_ec2():
    filter_by_kwargs = {}
    sort_by = None  # WISHLIST have a tuple
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            # ignore options
            continue
        if '=' in arg:
            key, value = arg.split('=', 2)
            if key not in HEADERS:
                exit('{} not valid'.format(key))
            filter_by_kwargs[key] = value
        elif arg in HEADERS:
            sort_by = arg
        else:
            print 'skipped', arg
    voyeur(sort_by=sort_by, filter_by=filter_by_kwargs)


if __name__ == '__main__':
    list_ec2()
