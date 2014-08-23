#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick n dirty CLI for checking ec2 inventory

Specifically design for my own personal workflow.
"""
from operator import attrgetter
import sys

from boto import ec2
from tabulate import tabulate
import boto.ec2.elb


def sort_key(key):
    """Get the accessor function for an instance to look for `key`."""
    # look for tags that match
    if key == 'name':
        return lambda x: x.tags.get('Name')
    if key in ('environment', 'site'):
        return lambda x: x.tags.get(key)
    # these are shortened for convenience
    if key == 'ip':
        return attrgetter('ip_address')
    if key == 'private_ip':
        return attrgetter('private_ip_address')
    # look for attributes that match
    return attrgetter(key)


def filter_key(filter_args):
    def filter_instance(instance):
        return all([value == sort_key(key)(instance)
            for key, value in filter_args.items()])
    return filter_instance


def voyeur(instances, to_row, sort_by=None, filter_by=None):
    if sort_by:
        instances.sort(key=sort_key(sort_by))
    if filter_by:
        instances = filter(filter_key(filter_by), instances)  # XXX overwriting original
    return map(to_row, instances)


def list_ec2(input_args):
    headers = (
        'name',
        'environment',
        'site',
        'ip',
        'private_ip',
        'launch_time',
        'id',
    )
    sort_by = None  # WISHLIST have a tuple
    filter_by_kwargs = {}
    for arg in input_args:
        if arg.startswith('-'):
            # ignore options
            continue
        if '=' in arg:
            key, value = arg.split('=', 2)
            if key not in headers:
                exit('{} not valid'.format(key))
            filter_by_kwargs[key] = value
        elif arg in headers:
            sort_by = arg
        else:
            print 'skipped', arg

    conn = ec2.connect_to_region('us-east-1')  # XXX magic constant
    instances = conn.get_only_instances()
    to_row = lambda x: (
        x.tags.get('Name'),
        x.tags.get('environment'),
        x.tags.get('site'),
        x.ip_address,
        x.private_ip_address,
        x.launch_time.split('T', 2)[0],
        x.id,
    )
    print tabulate(
        voyeur(instances, to_row=to_row, sort_by=sort_by, filter_by=filter_by_kwargs),
        headers=headers)


def list_elb(input_args):
    headers = (
        'name',
        'instance_count',
        'created_time',
    )

    sort_by = None
    filter_by_kwargs = {}

    conn = boto.ec2.elb.connect_to_region('us-east-1')  # XXX magic constant
    instances = conn.get_all_load_balancers()
    to_row = lambda x: (
        x.name,
        len(x.instances),
        x.created_time,
    )
    print tabulate(
        voyeur(instances, to_row=to_row, sort_by=sort_by, filter_by=filter_by_kwargs),
        headers=headers)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        list_ec2(sys.argv[1:])
    elif sys.argv[1] == 'ec2':
        list_ec2(sys.argv[2:])
    elif sys.argv[1] == 'elb':
        list_elb(sys.argv[2:])
    else:
        list_ec2(sys.argv[1:])
