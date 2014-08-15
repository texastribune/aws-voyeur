#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick n dirty CLI for checking ec2 inventory

Specifically design for my own personal workflow.

If you're doing something serious, you should look into these better
alternatives:

* https://github.com/DrGonzo65/ec2-cli-tools - very similar package that lets
  you glob
* https://github.com/mattrobenolt/ec2 - lets you query instances using django-
  orm-like syntax
* awscli - official aws cli

"""
import sys

from boto import ec2
from tabulate import tabulate


headers = (
    'name',
    'environment',
    'site',
    'ip',
    'private_ip',
    'launch_time',
    'id',
)


def to_row(instance):
    return (
        instance.tags.get('Name'),
        instance.tags.get('environment'),
        instance.tags.get('site'),
        instance.ip_address, instance.private_ip_address,
        instance.launch_time.split('T', 2)[0],
        instance.id,
        # instance.tags
    )


def sort_key(key):
    if key == 'name':
        return lambda x: x.tags.get('Name')
    if key in ('environment', 'site'):
        return lambda x: x.tags.get(key)
    return lambda x: getattr(x, key)


def filter_key(filter_args):
    def filter_instance(instance):
        return all([value == sort_key(key)(instance)
            for key, value in filter_args.items()])
    return filter_instance


def main(sort_by=None, filter_by=None):
    conn = ec2.connect_to_region('us-east-1')  # XXX magic constant

    instances = conn.get_only_instances()

    if sort_by:
        instances.sort(
            key=sort_key(sort_by),
        )
    if filter_by:
        instances = filter(filter_key(filter_by), instances)  # XXX modifying original

    print tabulate(map(to_row, instances), headers=headers)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if '=' in sys.argv[1]:
            key, value = sys.argv[1].split('=', 2)
            if key not in headers:
                exit('{} not valid'.format(key))
            main(filter_by={key: value})
        else:
            main(sort_by=sys.argv[1])
    else:
        main()
