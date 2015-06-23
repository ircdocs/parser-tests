#!/usr/bin/env python3
# Testing split.yaml with ircreactor and girc

# Written in 2015 by Daniel Oaks <daniel@danieloaks.net>
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

from ircreactor.envelope import RFC1459Message
from girc.utils import NickMask, validate_hostname
import ircmatch
import yaml


# SPLIT Tests
print('Running split tests')
data = yaml.safe_load(open('tests/msg-split.yaml').read())

failed_tests = 0
passed_tests = 0

for test in data['tests']:
    input = test['input']
    atoms = test['atoms']
    out = ' * Testing: [{}]\n'.format(input)

    m = RFC1459Message.from_message(input)
    failed = False

    # test atoms
    if 'tags' in atoms:
        if m.tags != atoms['tags']:
            out += '   Decoding tags failed, was [{}]\n'.format(m.tags)
            failed = True
    elif m.tags != {}:
        out += '   Decoding tags failed, was [{}]\n'.format(m.tags)
        failed = True

    if 'verb' in atoms:
        if m.verb.lower() != atoms['verb'].lower():
            out += '   Decoding verb failed, was [{}]\n'.format(m.verb.lower())
            failed = True
    elif m.verb.lower() != '':
        out += '   Decoding verb failed, was [{}]\n'.format(m.verb.lower())
        failed = True

    if 'source' in atoms:
        if m.source != atoms['source']:
            out += '   Decoding source failed, was [{}]\n'.format(m.source)
            failed = True
    elif m.source != None:
        out += '   Decoding source failed, was [{}]\n'.format(m.source)
        failed = True

    if 'params' in atoms:
        atom_params = list(atoms['params'])

        for param in m.params:
            if len(atom_params) < 1 or param != atom_params.pop(0):
                out += '   Decoding params failed, was {}\n'.format(m.params)
                failed = True
                break
    elif len(m.params):
        out += '   Decoding params failed\n'
        failed = True

    # fail message
    if failed:
        print(out)
        failed_tests += 1
    else:
        passed_tests += 1

print(' * Passed Tests:', passed_tests)
print(' * Failed Tests:', failed_tests)
print()


# JOIN Tests
print('Running join tests')
data = yaml.safe_load(open('tests/msg-join.yaml').read())

failed_tests = 0
passed_tests = 0

for test in data['tests']:
    atoms = test['atoms']
    matches = test['matches']
    out = ' * Testing: [{}]\n'.format(matches[0])

    failed = False
    m = RFC1459Message.from_data(atoms['verb'], **{
        'params': atoms.get('params'),
        'source': atoms.get('source'),
        'tags': atoms.get('tags', {}),
    })
    msg = m.to_message()

    # test atoms
    if msg not in matches:
        out += '   Joining message failed, got [{}]\n'.format(msg)
        failed = True
        break

    # fail message
    if failed:
        print(out)
        failed_tests += 1
    else:
        passed_tests += 1

print(' * Passed Tests:', passed_tests)
print(' * Failed Tests:', failed_tests)
print()


# NICKMASK Tests
print('Running nickmask tests')
data = yaml.safe_load(open('tests/mask-split.yaml').read())

failed_tests = 0
passed_tests = 0

for test in data['tests']:
    source = test['source']
    atoms = test['atoms']
    out = ' * Testing: [{}]\n'.format(source)

    nm = NickMask(source)
    failed = False

    # test atoms
    if 'nick' in atoms:
        if nm.nick != atoms['nick']:
            out += '   Decoding nick failed, was [{}]\n'.format(nm.nick)
            failed = True
    elif nm.nick != '':
        out += '   Decoding nick failed, was [{}]\n'.format(nm.nick)
        failed = True

    if 'user' in atoms:
        if nm.user != atoms['user']:
            out += '   Decoding user failed, was [{}]\n'.format(nm.user)
            failed = True
    elif nm.user != '':
        out += '   Decoding user failed, was [{}]\n'.format(nm.user)
        failed = True

    if 'host' in atoms:
        if nm.host != atoms['host']:
            out += '   Decoding host failed, was [{}]\n'.format(nm.host)
            failed = True
    elif nm.host != '':
        out += '   Decoding host failed, was [{}]\n'.format(nm.host)
        failed = True

    # fail message
    if failed:
        print(out)
        failed_tests += 1
    else:
        passed_tests += 1

print(' * Passed Tests:', passed_tests)
print(' * Failed Tests:', failed_tests)
print()


# HOSTNAME Tests
print('Running hostname tests')
data = yaml.safe_load(open('tests/validate-hostname.yaml').read())

failed_tests = 0
passed_tests = 0

for test in data['tests']:
    host = test['host']
    should_be_valid = test['valid']
    out = ' * Testing: [{}]\n'.format(host)

    is_valid = validate_hostname(host)
    failed = False

    # test validity
    if is_valid and not should_be_valid:
        out += '   Hostname validated successfully, but should have failed [{}]\n'.format(host)
        failed = True

    if should_be_valid and not is_valid:
        out += '   Hostname failed validation, but should have passed [{}]\n'.format(host)
        failed = True

    # fail message
    if failed:
        print(out)
        failed_tests += 1
    else:
        passed_tests += 1

print(' * Passed Tests:', passed_tests)
print(' * Failed Tests:', failed_tests)
print()


# MASK Tests
print('Running mask matching tests')
data = yaml.safe_load(open('tests/mask-match.yaml').read())

failed_tests = 0
passed_tests = 0

for test in data['tests']:
    mask = test['mask']
    matches = test['matches']
    invalid = test['fails']
    out = ' * Testing: [{}]\n'.format(mask)

    failed = False

    # test validity
    for address in matches:
        if not ircmatch.match(ircmatch.ascii, mask, address):
            out += '   Address did not match but should have [{}]\n'.format(address)
            failed = True

    for address in invalid:
        if ircmatch.match(ircmatch.ascii, mask, address):
            out += '   Address matched but should not have [{}]\n'.format(address)
            failed = True

    # fail message
    if failed:
        print(out)
        failed_tests += 1
    else:
        passed_tests += 1

print(' * Passed Tests:', passed_tests)
print(' * Failed Tests:', failed_tests)
