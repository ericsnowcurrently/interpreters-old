#! /usr/bin/env python3

import argparse
import configparser
import datetime
import os
import os.path
from urllib.request import urlretrieve


ROOT = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(ROOT, 'UPSTREAM')

SRC = [
        '/Modules/_xxsubinterpretersmodule.c',
        ]
INCLUDE = [
        '/pystate.h',
        '/pyatomic.h',
        '/pythread.h',
        '/internal/mem.h',
        '/internal/ceval.h',
        '/internal/warnings.h',
        '/internal/pystate.h',
        ]


def get_revision(repo, branch):
    raise NotImplementedError


def read_config(filename=CONFIG_FILE):
    print(filename)
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def write_config(config, filename):
    timestamp = datetime.datetime.utcnow()
    config['timestamp'] = timestamp.strftime('YYYY-MM-DD HH:MM:SS')
    with open(filename, 'w') as configfile:
        config.write(configfile)


def download(config, srcdir, includedir, log):
    'https://raw.github.com/python/cpython/master/Modules/_xxsubinterpretersmodule.c'
    baseurl = config['repo'].replace('github.com', 'raw.github.com')
    baseurl += '/' + config['revision']

    seendirs = set()

    log()
    log(' == downloading src files ==')
    for path in SRC:
        url = baseurl + path
        target = os.path.join(srcdir, os.path.basename(path))
        print(' + {}  <- {}'.format(target, url))
        dirname = os.path.dirname(target)
        if dirname not in seendirs:
            try:
                os.makedirs(dirname)
            except FileExistsError:
                pass
            seendirs.add(dirname)
        urlretrieve(url, target)

    log()
    log(' == downloading include files ==')
    for path in INCLUDE:
        url = baseurl + '/Include' + path
        target = includedir + path
        print(' + {}  <- {}'.format(target, url))
        dirname = os.path.dirname(target)
        if dirname not in seendirs:
            try:
                os.makedirs(dirname)
            except FileExistsError:
                pass
            seendirs.add(dirname)
        urlretrieve(url, target)


##################################
# the script

def parse_args(config=None):
    if config is None:
        config = read_config()
    parser = argparse.ArgumentParser()

    NO_WRITE = '<do not write the config>'
    parser.add_argument('--write', nargs='?')
    parser.add_argument('--no-write', dest='write',
                        action='store_const', const=NO_WRITE)

    parser.add_argument('--repo')
    parser.add_argument('-r', '--revision', '--rev')
    parser.add_argument('--branch')
    parser.add_argument('--srcdir', default='src')
    parser.add_argument('--includedir', default='include')

    args = parser.parse_args()

    if args.branch is not None:
        if args.revision is None:
            args.revision = get_revision(args.repo, args.branch)

    changed = False
    try:
        section = config['info']
    except KeyError:
        seciton = config['info'] = {}
    if args.repo is not None and args.repo != section.get('repo'):
        changed = True
        section['repo'] = args.repo
    if args.branch is not None and args.branch != section.get('branch'):
        changed = True
        section['branch'] = args.branch
    if args.revision is not None and args.revision != section.get('revision'):
        changed = True
        section['revision'] = args.revision

    configfile = args.write or None
    if configfile is NO_WRITE:
        configfile = None
    elif changed and not args.write:
        configfile = CONFIG_FILE

    return config, configfile, args.srcdir, args.includedir


def main(config, srcdir, includedir, filename=None):
    download(config['info'], srcdir, includedir, log=print)

    print()
    if filename is None:
        print('== not writing config ==')
    else:
        print('== writing config to {} =='.format(filename))
        write_config(config, filename)


if __name__ == '__main__':
    print('reading config')
    config = read_config()
    _, filename, srcdir, includedir = parse_args(config)
    main(config, srcdir, includedir, filename=filename)
