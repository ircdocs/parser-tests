# IRC Parser Tests

Various tests for IRC parsers so people can check to ensure they're consistent. These tests are based on existing test suites and widespread client behaviour.

**Note:** This is still being written. Feel free to suggest or contribute tests - PRs are welcomed!


## Testing

There are two included tests used to test these vectors, the Python and Golang programs.

### Using the python library
Either `pip install irc_parser_tests` or add `irc_parser_tests` to your `requirements.txt`. The test data is available in the module `parser_tests`.

### Releasing a new python version
1. Bump the version identifier in `parser_tests/__init__.py`
2. Commit the version bump and tag it `git tag v<version>`
3. Push to master
4. Github actions will deploy to PyPi

### Python

The `test.py` script uses the [girc](https://github.com/DanielOaks/girc) and [ircmatch](https://github.com/mammon-ircd/ircmatch>) libraries as reference implementations, as well as [pyyaml](http://pyyaml.org/) to parse the test files.

To install these libraries, run:

    pip3 install --upgrade girc ircmatch pyyaml

After that, simply run the script with `python3 test.py` in the root dir. This will test everything we can test, and show the output.


### Go

The `test.go` script uses the [girc-go](https://github.com/DanielOaks/girc-go) packages as reference implementations.

To install these packages, run:

    go get -u ./...

After that, simply run the script with `go run test.go run` in the root dir. This will test everything we can test, and show the output.


## Sources

Thanks to these sources for having open tests and/or agreeing to let me include your tests here!

Some tests originate from [Mozilla's test vectors](https://dxr.mozilla.org/comm-central/source/chat/protocols/irc/test/test_ircMessage.js), which are public domain.

Some tests originate from [grawity's test vectors](https://github.com/grawity/irc-parse-tests) which were WTFPL v2 licensed when they were retrieved.

Some tests originate from [Sadie's test vectors](https://github.com/SadieCat/ircparser-ruby/tree/master/test) which she's indicated I'm free to include here.
