#!/usr/bin/env python3
# Testing split.yaml with ircreactor and girc
from ircreactor.envelope import RFC1459Message
from girc.utils import NickMask, validate_hostname
import yaml


# SPLIT Tests
print('Running split tests')
data = yaml.safe_load(open('split.yaml').read())

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
        if m.verb.lower() != atoms['verb']:
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
            if param != atom_params.pop(0):
                out += '   Decoding params failed\n'
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


# NICKMASK Tests
print('Running nickmask tests')
data = yaml.safe_load(open('nickmask.yaml').read())

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
    elif nm.nick != '':
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
