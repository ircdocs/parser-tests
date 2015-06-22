#!/usr/bin/env python3
# Testing split.yaml with ircreactor
from ircreactor.envelope import RFC1459Message
import yaml

print('Running tests:')

# load test data
data = yaml.safe_load(open('split.yaml').read())

for test in data['tests']:
    input = test['input']
    atoms = test['atoms']

    print('Testing:', input)

    m = RFC1459Message.from_message(input)
    failed = False

    # test atoms
    if 'verb' in atoms:
        if m.verb.lower() != atoms['verb']:
            print('  *** Decoded verb failed, was [{}]'.format(m.verb.lower()))
            failed = True

    if 'source' in atoms:
        if m.source != atoms['source']:
            print('  *** Decoded source failed, was [{}]'.format(m.source))
            failed = True

    if 'params' in atoms:
        if m.params != atoms['params']:
            print('  *** Decoded params failed, was', m.params)

    # final message
    if failed:
        print(' FAIL\n')
