# IRC Parser Tests

Various tests for IRC parsers so people can check to ensure they're consistent. These tests are based on existing test suites and widespread client behaviour.

**Note:** This is still being written. Feel free to suggest or contribute tests - PRs are welcomed!


## Testing

There are two included tests used to test these vectors, the Python and Golang programs.

### Python

The `test.py` script uses the [girc](https://github.com/DanielOaks/girc) and [ircmatch](https://github.com/mammon-ircd/ircmatch>) libraries as reference implementations.

To install these libraries, run `pip3 install --upgrade girc ircmatch`.

After that, simply run `python3 test.py`. This will test everything we can test, and show the output.


## Sources

Some tests originate from [Mozilla's test vectors](https://dxr.mozilla.org/comm-central/source/chat/protocols/irc/test/test_ircMessage.js), which are public domain.

Some tests originate from [grawity's test vectors](https://github.com/grawity/code/tree/master/lib/tests) which were WTFPL v2 licensed when they were retrieved.
