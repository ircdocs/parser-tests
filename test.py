#!/usr/bin/env python3
# Testing split.yaml with ircreactor
from ircreactor.envelope import RFC1459Message
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
            out += '   Decoding tags failed, was [{}]\n'.format(m.tags.lower())
            failed = True

    if 'verb' in atoms:
        if m.verb.lower() != atoms['verb']:
            out += '   Decoding verb failed, was [{}]\n'.format(m.verb.lower())
            failed = True

    if 'source' in atoms:
        if m.source != atoms['source']:
            out += '   Decoding source failed, was [{}]\n'.format(m.source)
            failed = True

    if 'params' in atoms:
        atom_params = list(atoms['params'])

        for param in m.params:
            if param != atom_params.pop(0):
                out += '   Decoding params failed\n'
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
